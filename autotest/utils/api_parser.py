# -*- coding: utf-8 -*-
"""
API接口解析器 - 自动解析项目接口文档
"""

import re
import ast
import inspect
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from .logger import logger


class APIParser:
    """API接口解析器"""
    
    def __init__(self, main_file_path: str):
        """
        初始化API解析器
        
        Args:
            main_file_path: 主文件路径
        """
        self.main_file_path = main_file_path
        self.apis = []
    
    def parse_fastapi_routes(self) -> List[Dict[str, Any]]:
        """
        解析FastAPI路由
        
        Returns:
            API接口列表
        """
        try:
            with open(self.main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析AST
            tree = ast.parse(content)
            
            apis = []
            current_class = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 检查是否是API路由函数
                    api_info = self._extract_api_info(node, content)
                    if api_info:
                        apis.append(api_info)
            
            self.apis = apis
            logger.info(f"解析到 {len(apis)} 个API接口")
            return apis
            
        except Exception as e:
            logger.error(f"解析API接口失败: {e}")
            return []
    
    def _extract_api_info(self, node: ast.FunctionDef, content: str) -> Optional[Dict[str, Any]]:
        """
        提取API信息
        
        Args:
            node: 函数AST节点
            content: 源代码内容
            
        Returns:
            API信息字典
        """
        # 检查装饰器
        method = None
        path = None
        
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Attribute):
                # @app.get, @app.post等
                if isinstance(decorator.value, ast.Name) and decorator.value.id == 'app':
                    method = decorator.attr.upper()
                    # 获取路径参数
                    if node.decorator_list:
                        for dec in node.decorator_list:
                            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                                if dec.func.attr.lower() == method.lower():
                                    if dec.args and isinstance(dec.args[0], ast.Constant):
                                        path = dec.args[0].value
            elif isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    if isinstance(decorator.func.value, ast.Name) and decorator.func.value.id == 'app':
                        method = decorator.func.attr.upper()
                        # 获取路径参数
                        if decorator.args and isinstance(decorator.args[0], ast.Constant):
                            path = decorator.args[0].value
        
        if not method or not path:
            return None
        
        # 提取函数信息
        function_name = node.name
        docstring = ast.get_docstring(node) or ""
        
        # 解析参数
        parameters = self._extract_parameters(node)
        
        # 解析响应模型（从返回类型或文档字符串推断）
        response_model = self._extract_response_model(node, docstring)
        
        # 确定业务模块
        module = self._determine_module(path, function_name)
        
        return {
            'method': method,
            'path': path,
            'function_name': function_name,
            'description': docstring.split('\n')[0] if docstring else function_name,
            'parameters': parameters,
            'response_model': response_model,
            'module': module,
            'tags': self._extract_tags(path, docstring)
        }
    
    def _extract_parameters(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """
        提取函数参数信息
        
        Args:
            node: 函数AST节点
            
        Returns:
            参数列表
        """
        parameters = []
        
        for arg in node.args.args:
            if arg.arg in ['self', 'cls']:
                continue
            
            param_info = {
                'name': arg.arg,
                'type': 'str',  # 默认类型
                'required': True,
                'location': 'query'  # query, path, body
            }
            
            # 尝试从类型注解获取类型
            if arg.annotation:
                param_info['type'] = self._extract_type_from_annotation(arg.annotation)
            
            # 检查是否有默认值
            defaults_offset = len(node.args.args) - len(node.args.defaults)
            arg_index = node.args.args.index(arg)
            if arg_index >= defaults_offset:
                param_info['required'] = False
                default_index = arg_index - defaults_offset
                if default_index < len(node.args.defaults):
                    default_value = node.args.defaults[default_index]
                    if isinstance(default_value, ast.Constant):
                        param_info['default'] = default_value.value
            
            parameters.append(param_info)
        
        return parameters
    
    def _extract_type_from_annotation(self, annotation) -> str:
        """
        从类型注解提取类型
        
        Args:
            annotation: 类型注解AST节点
            
        Returns:
            类型字符串
        """
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        elif isinstance(annotation, ast.Subscript):
            # Optional[str], List[int]等
            if isinstance(annotation.value, ast.Name):
                return annotation.value.id
        
        return 'str'
    
    def _extract_response_model(self, node: ast.FunctionDef, docstring: str) -> Dict[str, Any]:
        """
        提取响应模型信息
        
        Args:
            node: 函数AST节点
            docstring: 文档字符串
            
        Returns:
            响应模型信息
        """
        # 默认响应结构
        response_model = {
            'type': 'object',
            'properties': {
                'code': {'type': 'integer', 'description': '响应码'},
                'message': {'type': 'string', 'description': '响应消息'},
                'data': {'type': 'object', 'description': '响应数据'}
            }
        }
        
        # TODO: 可以进一步解析返回类型注解或响应模型
        
        return response_model
    
    def _determine_module(self, path: str, function_name: str) -> str:
        """
        确定API所属的业务模块
        
        Args:
            path: API路径
            function_name: 函数名
            
        Returns:
            模块名
        """
        if '/medicines' in path:
            return 'medicine'
        elif '/patients' in path:
            return 'patient'
        elif '/consultations' in path:
            return 'consultation'
        elif '/doctors' in path:
            return 'doctor'
        elif '/appointments' in path:
            return 'appointment'
        else:
            return 'common'
    
    def _extract_tags(self, path: str, docstring: str) -> List[str]:
        """
        提取API标签
        
        Args:
            path: API路径
            docstring: 文档字符串
            
        Returns:
            标签列表
        """
        tags = []
        
        # 从路径提取
        if '/medicines' in path:
            tags.append('药物管理')
        elif '/patients' in path:
            tags.append('患者管理')
        elif '/consultations' in path:
            tags.append('就诊管理')
        elif '/doctors' in path:
            tags.append('医生管理')
        elif '/appointments' in path:
            tags.append('预约管理')
        
        # 从HTTP方法提取
        if 'stats' in path or 'summary' in path:
            tags.append('统计分析')
        
        return tags
    
    def get_apis_by_module(self, module: str) -> List[Dict[str, Any]]:
        """
        根据模块获取API列表
        
        Args:
            module: 模块名
            
        Returns:
            API列表
        """
        return [api for api in self.apis if api['module'] == module]
    
    def get_all_modules(self) -> List[str]:
        """
        获取所有模块名
        
        Returns:
            模块名列表
        """
        modules = set()
        for api in self.apis:
            modules.add(api['module'])
        return list(modules)
    
    def generate_test_scenarios(self, api: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        为API生成测试场景
        
        Args:
            api: API信息
            
        Returns:
            测试场景列表
        """
        scenarios = []
        
        # 正常场景
        scenarios.append({
            'name': f"{api['description']} - 正常场景",
            'type': 'positive',
            'priority': 'high',
            'description': f"测试{api['description']}的正常功能",
            'method': api['method'],
            'path': api['path'],
            'parameters': self._generate_valid_params(api['parameters']),
            'expected_status': 200
        })
        
        # 参数缺失场景
        required_params = [p for p in api['parameters'] if p['required']]
        if required_params:
            scenarios.append({
                'name': f"{api['description']} - 缺失必填参数",
                'type': 'negative',
                'priority': 'medium',
                'description': f"测试{api['description']}缺失必填参数的情况",
                'method': api['method'],
                'path': api['path'],
                'parameters': {},
                'expected_status': 422
            })
        
        # 参数类型错误场景
        if api['parameters']:
            scenarios.append({
                'name': f"{api['description']} - 参数类型错误",
                'type': 'negative',
                'priority': 'medium',
                'description': f"测试{api['description']}参数类型错误的情况",
                'method': api['method'],
                'path': api['path'],
                'parameters': self._generate_invalid_params(api['parameters']),
                'expected_status': 422
            })
        
        # 权限测试场景（如果适用）
        if api['method'] in ['POST', 'PUT', 'DELETE']:
            scenarios.append({
                'name': f"{api['description']} - 权限测试",
                'type': 'security',
                'priority': 'medium',
                'description': f"测试{api['description']}的权限控制",
                'method': api['method'],
                'path': api['path'],
                'parameters': self._generate_valid_params(api['parameters']),
                'expected_status': 401
            })
        
        return scenarios
    
    def _generate_valid_params(self, parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成有效参数
        
        Args:
            parameters: 参数列表
            
        Returns:
            参数字典
        """
        params = {}
        for param in parameters:
            if param['type'] == 'int':
                params[param['name']] = 1
            elif param['type'] == 'float':
                params[param['name']] = 1.0
            elif param['type'] == 'bool':
                params[param['name']] = True
            else:
                params[param['name']] = 'test_value'
        
        return params
    
    def _generate_invalid_params(self, parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成无效参数
        
        Args:
            parameters: 参数列表
            
        Returns:
            参数字典
        """
        params = {}
        for param in parameters:
            if param['type'] == 'int':
                params[param['name']] = 'invalid_int'
            elif param['type'] == 'float':
                params[param['name']] = 'invalid_float'
            elif param['type'] == 'bool':
                params[param['name']] = 'invalid_bool'
            else:
                params[param['name']] = 12345  # 数字代替字符串
        
        return params