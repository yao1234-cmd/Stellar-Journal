# -*- coding: utf-8 -*-
"""
断言助手 - 提供常用的断言方法
"""

import json
from typing import Any, Dict, List, Union
from requests import Response
from .logger import logger
import allure


class AssertionHelper:
    """断言助手类"""
    
    @staticmethod
    def assert_status_code(response: Response, expected_code: int, message: str = None):
        """
        断言HTTP状态码
        
        Args:
            response: HTTP响应对象
            expected_code: 期望的状态码
            message: 自定义错误消息
        """
        actual_code = response.status_code
        error_msg = message or f"期望状态码 {expected_code}，实际状态码 {actual_code}"
        
        with allure.step(f"断言状态码为 {expected_code}"):
            assert actual_code == expected_code, error_msg
            logger.info(f"状态码断言通过: {actual_code}")
    
    @staticmethod
    def assert_response_time(response: Response, max_time: float, message: str = None):
        """
        断言响应时间
        
        Args:
            response: HTTP响应对象
            max_time: 最大响应时间（秒）
            message: 自定义错误消息
        """
        actual_time = response.elapsed.total_seconds()
        error_msg = message or f"响应时间 {actual_time}s 超过限制 {max_time}s"
        
        with allure.step(f"断言响应时间小于 {max_time}s"):
            assert actual_time <= max_time, error_msg
            logger.info(f"响应时间断言通过: {actual_time}s")
    
    @staticmethod
    def assert_json_structure(response: Response, expected_keys: List[str], message: str = None):
        """
        断言JSON响应结构
        
        Args:
            response: HTTP响应对象
            expected_keys: 期望的键列表
            message: 自定义错误消息
        """
        try:
            json_data = response.json()
        except json.JSONDecodeError:
            raise AssertionError("响应不是有效的JSON格式")
        
        missing_keys = []
        for key in expected_keys:
            if key not in json_data:
                missing_keys.append(key)
        
        error_msg = message or f"响应JSON缺少字段: {missing_keys}"
        
        with allure.step(f"断言JSON包含字段: {expected_keys}"):
            assert not missing_keys, error_msg
            logger.info(f"JSON结构断言通过: {expected_keys}")
    
    @staticmethod
    def assert_json_value(response: Response, key_path: str, expected_value: Any, message: str = None):
        """
        断言JSON中指定路径的值
        
        Args:
            response: HTTP响应对象
            key_path: 键路径，支持点号分隔的嵌套路径，如 'data.user.name'
            expected_value: 期望值
            message: 自定义错误消息
        """
        try:
            json_data = response.json()
        except json.JSONDecodeError:
            raise AssertionError("响应不是有效的JSON格式")
        
        # 解析嵌套路径
        keys = key_path.split('.')
        actual_value = json_data
        
        try:
            for key in keys:
                if isinstance(actual_value, dict):
                    actual_value = actual_value[key]
                elif isinstance(actual_value, list) and key.isdigit():
                    actual_value = actual_value[int(key)]
                else:
                    raise KeyError(f"路径 '{key_path}' 不存在")
        except (KeyError, IndexError, TypeError):
            raise AssertionError(f"JSON路径 '{key_path}' 不存在")
        
        error_msg = message or f"路径 '{key_path}' 的值期望为 {expected_value}，实际为 {actual_value}"
        
        with allure.step(f"断言 {key_path} = {expected_value}"):
            assert actual_value == expected_value, error_msg
            logger.info(f"JSON值断言通过: {key_path} = {actual_value}")
    
    @staticmethod
    def assert_json_contains(response: Response, key_path: str, expected_substring: str, message: str = None):
        """
        断言JSON中指定路径的值包含指定子字符串
        
        Args:
            response: HTTP响应对象
            key_path: 键路径
            expected_substring: 期望包含的子字符串
            message: 自定义错误消息
        """
        try:
            json_data = response.json()
        except json.JSONDecodeError:
            raise AssertionError("响应不是有效的JSON格式")
        
        # 解析嵌套路径
        keys = key_path.split('.')
        actual_value = json_data
        
        try:
            for key in keys:
                actual_value = actual_value[key]
        except KeyError:
            raise AssertionError(f"JSON路径 '{key_path}' 不存在")
        
        actual_str = str(actual_value)
        error_msg = message or f"路径 '{key_path}' 的值 '{actual_str}' 不包含 '{expected_substring}'"
        
        with allure.step(f"断言 {key_path} 包含 '{expected_substring}'"):
            assert expected_substring in actual_str, error_msg
            logger.info(f"JSON包含断言通过: {key_path} 包含 '{expected_substring}'")
    
    @staticmethod
    def assert_list_length(response: Response, key_path: str, expected_length: int, message: str = None):
        """
        断言JSON中指定路径的列表长度
        
        Args:
            response: HTTP响应对象
            key_path: 键路径
            expected_length: 期望长度
            message: 自定义错误消息
        """
        try:
            json_data = response.json()
        except json.JSONDecodeError:
            raise AssertionError("响应不是有效的JSON格式")
        
        # 解析嵌套路径
        keys = key_path.split('.')
        actual_list = json_data
        
        try:
            for key in keys:
                actual_list = actual_list[key]
        except KeyError:
            raise AssertionError(f"JSON路径 '{key_path}' 不存在")
        
        if not isinstance(actual_list, list):
            raise AssertionError(f"路径 '{key_path}' 的值不是列表类型")
        
        actual_length = len(actual_list)
        error_msg = message or f"列表长度期望为 {expected_length}，实际为 {actual_length}"
        
        with allure.step(f"断言列表 {key_path} 长度为 {expected_length}"):
            assert actual_length == expected_length, error_msg
            logger.info(f"列表长度断言通过: {key_path} 长度为 {actual_length}")
    
    @staticmethod
    def assert_list_not_empty(response: Response, key_path: str, message: str = None):
        """
        断言JSON中指定路径的列表不为空
        
        Args:
            response: HTTP响应对象
            key_path: 键路径
            message: 自定义错误消息
        """
        try:
            json_data = response.json()
        except json.JSONDecodeError:
            raise AssertionError("响应不是有效的JSON格式")
        
        # 解析嵌套路径
        keys = key_path.split('.')
        actual_list = json_data
        
        try:
            for key in keys:
                actual_list = actual_list[key]
        except KeyError:
            raise AssertionError(f"JSON路径 '{key_path}' 不存在")
        
        if not isinstance(actual_list, list):
            raise AssertionError(f"路径 '{key_path}' 的值不是列表类型")
        
        error_msg = message or f"列表 '{key_path}' 为空"
        
        with allure.step(f"断言列表 {key_path} 不为空"):
            assert len(actual_list) > 0, error_msg
            logger.info(f"列表非空断言通过: {key_path} 包含 {len(actual_list)} 个元素")
    
    @staticmethod
    def assert_headers_contain(response: Response, expected_headers: Dict[str, str], message: str = None):
        """
        断言响应头包含指定的头信息
        
        Args:
            response: HTTP响应对象
            expected_headers: 期望的头信息字典
            message: 自定义错误消息
        """
        missing_headers = []
        incorrect_headers = []
        
        for header_name, expected_value in expected_headers.items():
            if header_name not in response.headers:
                missing_headers.append(header_name)
            elif response.headers[header_name] != expected_value:
                incorrect_headers.append({
                    'name': header_name,
                    'expected': expected_value,
                    'actual': response.headers[header_name]
                })
        
        error_msg = message or f"缺少头信息: {missing_headers}, 错误头信息: {incorrect_headers}"
        
        with allure.step(f"断言响应头包含: {expected_headers}"):
            assert not missing_headers and not incorrect_headers, error_msg
            logger.info(f"响应头断言通过: {expected_headers}")


# 全局断言助手实例
assert_helper = AssertionHelper()