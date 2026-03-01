# -*- coding: utf-8 -*-
"""
HTTP 客户端 - 统一请求封装

与 autotest 框架保持一致风格，额外支持：
  - set_bearer_token()：为 session 设置 Authorization 头（Stellar-Journal 需要鉴权）
  - clear_token()：移除 token（用于测试未认证场景）
"""
import json
import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Optional

from .config_manager import config
from .logger import logger


class HTTPClient:
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = (base_url or config.get_base_url()).rstrip("/")
        self.timeout = timeout or config.get_timeout()
        self.session = requests.Session()

        # 重试策略：遇到服务端 5xx / 限流 429 时自动重试
        retry = Retry(
            total=config.get_retry_count(),
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    # -------------------------------------------------------------------------
    # Token 管理
    # -------------------------------------------------------------------------
    def set_bearer_token(self, token: str) -> None:
        """设置 Bearer token，之后所有请求都会带此 Authorization 头"""
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.info("已设置 Bearer token")

    def clear_token(self) -> None:
        """移除 Authorization 头，用于测试「未登录 → 401」的场景"""
        self.session.headers.pop("Authorization", None)
        logger.info("已清除 Bearer token")

    # -------------------------------------------------------------------------
    # 日志 / Allure 附件
    # -------------------------------------------------------------------------
    def _log_request(self, method: str, url: str, **kwargs) -> None:
        logger.info(f"[REQUEST] {method.upper()} {url}")
        if "json" in kwargs:
            logger.info(f"  body : {json.dumps(kwargs['json'], ensure_ascii=False)}")
        if "params" in kwargs:
            logger.info(f"  params: {kwargs['params']}")

    def _log_response(self, response: requests.Response) -> None:
        logger.info(f"[RESPONSE] {response.status_code} | {response.elapsed.total_seconds():.3f}s")
        try:
            logger.info(f"  body : {json.dumps(response.json(), ensure_ascii=False)}")
        except Exception:
            logger.info(f"  body : {response.text[:500]}")

    def _attach_allure(self, method: str, url: str, response: requests.Response, **kwargs) -> None:
        allure.attach(f"{method.upper()} {url}", name="请求地址", attachment_type=allure.attachment_type.TEXT)
        if "json" in kwargs:
            allure.attach(
                json.dumps(kwargs["json"], ensure_ascii=False, indent=2),
                name="请求体",
                attachment_type=allure.attachment_type.JSON,
            )
        if "params" in kwargs:
            allure.attach(
                json.dumps(kwargs["params"], ensure_ascii=False, indent=2),
                name="查询参数",
                attachment_type=allure.attachment_type.JSON,
            )
        allure.attach(str(response.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
        try:
            allure.attach(
                json.dumps(response.json(), ensure_ascii=False, indent=2),
                name="响应体",
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            allure.attach(response.text, name="响应体", attachment_type=allure.attachment_type.TEXT)

    # -------------------------------------------------------------------------
    # 核心请求方法
    # -------------------------------------------------------------------------
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        self._log_request(method, url, **kwargs)
        response = self.session.request(method, url, **kwargs)
        self._log_response(response)
        self._attach_allure(method, url, response, **kwargs)

        return response

    def get(self, endpoint: str, params: Dict = None, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json_data: Dict = None, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, json=json_data, **kwargs)

    def put(self, endpoint: str, json_data: Dict = None, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, json=json_data, **kwargs)

    def patch(self, endpoint: str, json_data: Dict = None, **kwargs) -> requests.Response:
        return self.request("PATCH", endpoint, json=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)


# 全局默认客户端实例（不带 token，conftest 登录后会 set_bearer_token）
http_client = HTTPClient()
