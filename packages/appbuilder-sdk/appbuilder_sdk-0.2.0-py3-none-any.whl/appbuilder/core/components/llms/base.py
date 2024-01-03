# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import uuid
from enum import Enum

import requests
from appbuilder.core.constants import GATEWAY_URL, GATEWAY_INNER_URL
from pydantic import BaseModel, Field, ValidationError, HttpUrl, validator
from pydantic.types import confloat

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.utils.logger_util import logger
from typing import Dict, List, Optional, Any

from appbuilder.core.component import ComponentArguments
from appbuilder.core._exception import AppBuilderServerException


class CompletionRequest(object):
    r"""ShortSpeechRecognitionRequest."""
    params = None
    response_mode = "blocking"

    def __init__(self, params: Dict[str, Any] = None, response_mode: str = None, **kwargs):
        r""" __init__ the client state.
        """
        self.params = params
        self.response_mode = response_mode


class ModelArgsConfig(BaseModel):
    stream: bool = Field(default=False, description="是否流式响应。默认为 False。")
    temperature: confloat(gt=0.0, le=1.0) = Field(default=1e-10, description="模型的温度参数，范围从 0.0 到 1.0。")


class ModelDefineConfig(BaseModel):
    model: Optional[str] = Field(..., description="模型的名称")

    @validator("model")
    def check_and_convert_name(cls, v):
        """检查并转换模型真实调用。
        
        Args:
            cls (Any): 无用参数，仅在方法内部使用。
            v (str): 需要验证和转换的真实调用URL。
        
        Returns:
            str: 返回转换后的模型名称，如果输入的模型名称不在预定义映射表中则抛出ValueError异常。
        
        Raises:
            ValueError: 如果输入的模型名称不在预定义映射表中，则抛出此异常。
        
        """
        name_mapping = {
            "ernie-bot": '{}/rpc/2.0/cloud_hub/v1/bce/wenxinworkshop/ai_custom/v1'
                         '/chat/completions'.format(GATEWAY_INNER_URL),
            "ernie-bot-4": '{}/rpc/2.0/cloud_hub/v1/bce/wenxinworkshop/ai_custom/v1'
                           '/chat/completions_pro'.format(GATEWAY_INNER_URL),
            "eb-turbo-appbuilder": '{}/rpc/2.0/cloud_hub/v1/bce/wenxinworkshop/ai_custom/v1/'
                                   'chat/ai_apaas'.format(GATEWAY_INNER_URL)
        }

        if v not in name_mapping:
            allowed_names = ", ".join(name_mapping.keys())
            raise ValueError(f"model name must be one of [{allowed_names}]")

        return name_mapping[v]


class CompletionResponse(object):
    r"""ShortSpeechRecognitionResponse."""
    error_no = 0
    error_msg = ""
    result = None
    log_id = ""

    def __init__(self, response, stream: bool = False):
        """初始化客户端状态。"""
        self.error_no = 0
        self.error_msg = ""
        self.log_id = response.headers.get("X-Appbuilder-Request-Id", None)

        if stream:
            # 流式数据处理
            def stream_data():
                for chunk in response.iter_content(chunk_size=None):
                    answer = self.parse_stream_data(chunk)
                    if answer is not None:
                        yield answer

            self.result = stream_data()
        else:
            # 非流式数据的处理
            if response.status_code != 200:
                self.error_no = response.status_code
                self.error_msg = "error"
                self.result = response.text

                raise AppBuilderServerException(self.log_id, self.error_no, self.result)

            else:
                data = response.json()

                if "code" in data and "message" in data and "requestId" in data:
                    raise AppBuilderServerException(self.log_id, data["code"], data["message"])

                if "code" in data and "message" in data and "status" in data:
                    raise AppBuilderServerException(self.log_id, data["code"], data["message"])

                self.result = data.get("answer", None)

    def parse_stream_data(self, data_chunk):
        """解析流式数据块并提取answer字段"""

        data_str = data_chunk.decode('utf-8')

        if data_str.startswith("data: "):
            parsed_str = data_str[6:]
        else:
            parsed_str = data_str

        print("xxx: " + parsed_str)

        try:
            data = json.loads(parsed_str)

            if "code" in data and "message" in data and "requestId" in data:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            if "code" in data and "message" in data and "status" in data:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            return data.get("answer", "")
        except json.JSONDecodeError:
            # 处理可能的解析错误
            print("error: " + parsed_str)
            raise AppBuilderServerException("unknown", "unknown", parsed_str)

    def get_stream_data(self):
        """获取处理过的流式数据的迭代器"""
        return self.result

    def to_message(self):
        """将响应结果转换为Message对象。

        Returns:
            Message: Message对象。

        """
        message = Message()
        message.id = self.log_id
        message.content = self.result
        return message


class CompletionBaseComponent(Component):
    name: str
    version: str
    base_url: str = "/rpc/2.0/cloud_hub/v1/ai_engine/copilot_engine"
    model_name: str = ""
    model_url: str = ""

    model_config: Dict[str, Any] = {
        "model": {
            "provider": "baidu",
            "name": "ERNIE-Bot",
            "completion_params": {
                "temperature": 1e-10,
                "top_p": 0,
                "presence_penalty": 0,
                "frequency_penalty": 0
            }
        }
    }

    def __init__(self, meta: ComponentArguments, model=None, secret_key: Optional[str] = None,
                 gateway: str = ""):
        """
        Args:
            meta (ComponentArguments): 组件参数信息
            model (str, optional): 模型名称. Defaults to None.
            secret_key (Optional[str], optional): 可选的密钥. Defaults to None.
            gateway (str, optional): 网关地址. Defaults to "".
        
        """
        super().__init__(meta=meta, secret_key=secret_key, gateway=gateway)

        model_config_inputs = ModelDefineConfig(**{"model": model})

        self.model_name = model
        self.model_url = model_config_inputs.model

        if not self.model_url and not self.model_name:
            raise ValueError("model_name or model_url must be provided")

        self.version = self.version

    def gene_request(self, query, inputs, response_mode, message_id, model_config):
        """"send request"""

        data = {
            "query": query,
            "inputs": inputs,
            "response_mode": response_mode,
            "user": message_id,
            "model_config": model_config
        }

        request = CompletionRequest(data, response_mode)
        return request

    def gene_response(self, response, stream: bool = False):
        """generate response"""
        response = CompletionResponse(response, stream)
        return response

    def run(self, *args, **kwargs):
        """
        Run the model with given input and return the result.

        Args:
            **kwargs: Keyword arguments for both StyleWritingComponent and common component inputs.

        Returns:
            obj:`Message`: Output message after running model.
        """

        specific_params = {k: v for k, v in kwargs.items() if k in self.meta.__fields__}
        model_config_params = {k: v for k, v in kwargs.items() if k in ModelArgsConfig.__fields__}

        try:
            specific_inputs = self.meta(**specific_params)
            model_config_inputs = ModelArgsConfig(**model_config_params)
        except ValidationError as e:
            raise ValueError(e)

        query, inputs, response_mode, user_id = self.get_compeliton_params(specific_inputs, model_config_inputs)
        model_config = self.get_model_config(model_config_inputs)
        request = self.gene_request(query, inputs, response_mode, user_id, model_config)
        response = self.completion(self.version, self.base_url, request)

        if response.error_no != 0:
            raise AppBuilderServerException(service_err_code=response.error_no, service_err_message=response.error_msg)

        return response.to_message()

    def get_compeliton_params(self, specific_inputs, model_config_inputs):
        """获取模型请求参数"""
        inputs = specific_inputs.extract_values_to_dict()

        query = inputs["query"]
        user_id = str(uuid.uuid4())

        if model_config_inputs.stream:
            response_mode = "streaming"
        else:
            response_mode = "blocking"

        return query, inputs, response_mode, user_id

    def get_model_config(self, model_config_inputs):
        """获取模型配置信息"""
        if self.model_url:
            self.model_config["model"]["url"] = self.model_url

        if self.model_name:
            self.model_config["model"]["name"] = self.model_name

        self.model_config["model"]["completion_params"]["temperature"] = model_config_inputs.temperature
        return self.model_config

    def completion(self, version, base_url, request: CompletionRequest, timeout: float = None,
                   retry: int = 0, ) -> CompletionResponse:
        r"""Send a byte array of an audio file to obtain the result of speech recognition."""

        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        completion_url = "/" + self.version + "/api/llm/" + self.name

        stream = True if request.response_mode == "streaming" else False
        url = self.http_client.service_url(completion_url, self.base_url)

        logger.debug(
            "request url: {}, method: {}, json: {}, headers: {}".format(url,
                                                                        "POST",
                                                                        request.params,
                                                                        headers))

        response = self.http_client.session.post(url, json=request.params, headers=headers, timeout=timeout, stream=stream)

        logger.debug(
            "request url: {}, method: {}, json: {}, headers: {}, response: {}".format(url, "POST",
                                                                                      request.params,
                                                                                      headers,
                                                                                      response))
        return self.gene_response(response, stream)

    @staticmethod
    def check_service_error(data: dict):
        r"""check service internal error.
            :param: data: dict, service return body data.
            :rtype: .
        """
        if "err_no" in data and "err_msg" in data:
            if data["err_no"] != 0:
                raise AppBuilderServerException(service_err_code=data["err_no"], service_err_message=data["err_msg"])
