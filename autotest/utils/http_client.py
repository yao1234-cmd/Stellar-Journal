# -*- coding: utf-8 -*-
"""
HTTP客户端 - 统一的API请求处理
"""

import requests
import json
import allure
from typing import Dict, Any, Optional, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .config_manager import config
from .logger import logger


class HTTPClient:
    """HTTP客户端"""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        """
        初始化HTTP客户端
        
        Args:
            base_url: 基础URL
            timeout: 请求超时时间
        """
        self.base_url = base_url or config.get_base_url()
        self.timeout = timeout or config.get_timeout()
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=config.get_retry_count(),
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置默认headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求信息"""
        logger.info(f"发送请求: {method.upper()} {url}")
        if 'json' in kwargs:
            logger.info(f"请求体: {json.dumps(kwargs['json'], ensure_ascii=False, indent=2)}")
        if 'params' in kwargs:
            logger.info(f"查询参数: {kwargs['params']}")
    
    def _log_response(self, response: requests.Response):
        """记录响应信息"""
        logger.info(f"响应状态码: {response.status_code}")
        try:
            response_json = response.json()
            logger.info(f"响应体: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
        except:
            logger.info(f"响应体: {response.text}")
    
    def _attach_allure_info(self, method: str, url: str, response: requests.Response, **kwargs):
        """附加Allure报告信息"""
        # 附加请求信息
        allure.attach(
            f"{method.upper()} {url}",
            name="请求URL",
            attachment_type=allure.attachment_type.TEXT
        )
        
        if 'json' in kwargs:
            allure.attach(
                json.dumps(kwargs['json'], ensure_ascii=False, indent=2),
                name="请求体",
                attachment_type=allure.attachment_type.JSON
            )
        
        if 'params' in kwargs:
            allure.attach(
                json.dumps(kwargs['params'], ensure_ascii=False, indent=2),
                name="查询参数",
                attachment_type=allure.attachment_type.JSON
            )
        
        # 附加响应信息
        allure.attach(
            str(response.status_code),
            name="响应状态码",
            attachment_type=allure.attachment_type.TEXT
        )
        
        try:
            response_json = response.json()
            allure.attach(
                json.dumps(response_json, ensure_ascii=False, indent=2),
                name="响应体",
                attachment_type=allure.attachment_type.JSON
            )
        except:
            allure.attach(
                response.text,
                name="响应体",
                attachment_type=allure.attachment_type.TEXT
            )
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            **kwargs: requests参数
            
        Returns:
            响应对象
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # 设置默认超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        # 记录请求信息
        self._log_request(method, url, **kwargs)
        
        # 发送请求
        response = self.session.request(method, url, **kwargs)
        
        # 记录响应信息
        self._log_response(response)
        
        # 附加Allure信息
        self._attach_allure_info(method, url, response, **kwargs)
        
        return response
    
    def get(self, endpoint: str, params: Dict = None, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, json_data: Dict = None, **kwargs) -> requests.Response:
        """POST请求"""
        return self.request('POST', endpoint, json=json_data, **kwargs)
    
    def put(self, endpoint: str, json_data: Dict = None, **kwargs) -> requests.Response:
        """PUT请求"""
        return self.request('PUT', endpoint, json=json_data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, json_data: Dict = None, **kwargs) -> requests.Response:
        """PATCH请求"""
        return self.request('PATCH', endpoint, json=json_data, **kwargs)


# 全局HTTP客户端实例
http_client = HTTPClient()