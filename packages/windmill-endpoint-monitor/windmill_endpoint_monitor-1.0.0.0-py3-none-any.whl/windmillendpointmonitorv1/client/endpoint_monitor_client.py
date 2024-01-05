# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/9/15 14:13
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : endpoint_client.py
# @Software: PyCharm
"""
from typing import Optional
from baidubce.http import http_methods
from baidubce.http import http_content_types
from baidubce.bce_base_client import BceBaseClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce import compat
from baidubce.auth import bce_v1_signer


class EndpointMonitorClient(BceBaseClient):
    """
    A client class for interacting with the endpoint service. Initializes with default configuration.

    This client provides an interface to interact with the endpoint service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving endpoint within a specified workspace.

    Args:
        config (Optional[BceClientConfiguration]): The client configuration to use.
        ak (Optional[str]): Access key for authentication.
        sk (Optional[str]): Secret key for authentication.
        endpoint (Optional[str]): The service endpoint URL.
    """

    def __init__(self, config: Optional[BceClientConfiguration] = None, ak: Optional[str] = "",
                 sk: Optional[str] = "", endpoint: Optional[str] = ""):
        """
        init the client with default configuration
        """
        if config is None:
            config = BceClientConfiguration(credentials=BceCredentials(ak, sk), endpoint=endpoint)
        super(EndpointMonitorClient, self).__init__(config=config)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        """
        send http request with headers and params
        """
        return bce_http_client.send_request(self.config, sign_wrapper([b'host', b'x-bce-date']),
                                            [handler.parse_json],
                                            http_method, path, body, headers, params)

    def get_endpoint_status(self, workspace_id: str, endpoint_hub_name: str, local_name: str):
        """
        get endpoint in the system.

        Args:
            workspace_id (str): 工作区 id
            endpoint_hub_name (str): 端点中心名称
            local_name: 名称
        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + endpoint_hub_name + "/endpoints/"
                                             + local_name + "/endpointstatus", encoding="utf-8"))


def sign_wrapper(headers_to_sign):
    """wrapper the bce_v1_signer.sign()."""

    def _wrapper(credentials, http_method, path, headers, params):
        credentials.access_key_id = compat.convert_to_bytes(credentials.access_key_id)
        credentials.secret_access_key = compat.convert_to_bytes(credentials.secret_access_key)

        return bce_v1_signer.sign(credentials,
                                  compat.convert_to_bytes(http_method),
                                  compat.convert_to_bytes(path), headers, params,
                                  headers_to_sign=headers_to_sign)

    return _wrapper
