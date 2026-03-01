# -*- coding: utf-8 -*-
"""
断言工具 - 常用断言封装（与 autotest 风格保持一致）
"""
import json
import re
import allure
from typing import Any, Dict, List
from requests import Response
from .logger import logger


class AssertionHelper:

    @staticmethod
    def assert_status_code(response: Response, expected: int, message: str = None) -> None:
        actual = response.status_code
        msg = message or f"期望状态码 {expected}，实际 {actual}"
        with allure.step(f"断言状态码 == {expected}"):
            assert actual == expected, msg
            logger.info(f"状态码断言通过: {actual}")

    @staticmethod
    def assert_response_time(response: Response, max_seconds: float, message: str = None) -> None:
        actual = response.elapsed.total_seconds()
        msg = message or f"响应时间 {actual:.3f}s 超过限制 {max_seconds}s"
        with allure.step(f"断言响应时间 < {max_seconds}s"):
            assert actual <= max_seconds, msg
            logger.info(f"响应时间断言通过: {actual:.3f}s")

    @staticmethod
    def assert_json_keys(response: Response, keys: List[str], message: str = None) -> None:
        """断言响应 JSON 的顶层包含指定所有 key"""
        data = response.json()
        missing = [k for k in keys if k not in data]
        msg = message or f"响应 JSON 缺少字段: {missing}"
        with allure.step(f"断言响应含字段: {keys}"):
            assert not missing, msg
            logger.info(f"JSON 字段断言通过: {keys}")

    @staticmethod
    def assert_json_value(response: Response, key_path: str, expected: Any, message: str = None) -> None:
        """断言 JSON 指定路径（点号）的值，如 'emotion_analysis.valence'"""
        data = response.json()
        actual = data
        try:
            for k in key_path.split("."):
                actual = actual[int(k)] if isinstance(actual, list) else actual[k]
        except (KeyError, IndexError, TypeError):
            raise AssertionError(f"JSON 路径 '{key_path}' 不存在")
        msg = message or f"路径 '{key_path}' 期望 {expected}，实际 {actual}"
        with allure.step(f"断言 {key_path} == {expected}"):
            assert actual == expected, msg
            logger.info(f"JSON 值断言通过: {key_path} = {actual}")

    @staticmethod
    def assert_json_not_none(response: Response, key_path: str, message: str = None) -> None:
        """断言 JSON 指定路径的值不为 None"""
        data = response.json()
        actual = data
        try:
            for k in key_path.split("."):
                actual = actual[int(k)] if isinstance(actual, list) else actual[k]
        except (KeyError, IndexError, TypeError):
            raise AssertionError(f"JSON 路径 '{key_path}' 不存在")
        msg = message or f"路径 '{key_path}' 的值为 None"
        with allure.step(f"断言 {key_path} 不为 None"):
            assert actual is not None, msg
            logger.info(f"JSON 非 None 断言通过: {key_path} = {actual}")

    @staticmethod
    def assert_list_not_empty(response: Response, key_path: str, message: str = None) -> None:
        """断言 JSON 指定路径是非空列表"""
        data = response.json()
        actual = data
        try:
            for k in key_path.split("."):
                actual = actual[int(k)] if isinstance(actual, list) else actual[k]
        except (KeyError, IndexError, TypeError):
            raise AssertionError(f"JSON 路径 '{key_path}' 不存在")
        msg = message or f"路径 '{key_path}' 的列表为空"
        with allure.step(f"断言 {key_path} 非空列表"):
            assert isinstance(actual, list) and len(actual) > 0, msg
            logger.info(f"非空列表断言通过: {key_path} 含 {len(actual)} 项")

    @staticmethod
    def assert_field_type(response: Response, key_path: str, expected_type: type, message: str = None) -> None:
        """断言字段是指定类型"""
        data = response.json()
        actual = data
        try:
            for k in key_path.split("."):
                actual = actual[int(k)] if isinstance(actual, list) else actual[k]
        except (KeyError, IndexError, TypeError):
            raise AssertionError(f"JSON 路径 '{key_path}' 不存在")
        msg = message or f"路径 '{key_path}' 期望类型 {expected_type.__name__}，实际 {type(actual).__name__}"
        with allure.step(f"断言 {key_path} 类型为 {expected_type.__name__}"):
            assert isinstance(actual, expected_type), msg
            logger.info(f"类型断言通过: {key_path} 是 {expected_type.__name__}")


assert_helper = AssertionHelper()
