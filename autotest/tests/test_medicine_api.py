# -*- coding: utf-8 -*-
"""
药物管理API测试用例
"""

import pytest
import allure
from utils.http_client import HTTPClient
from utils.assertion_helper import assert_helper
from utils.data_generator import data_generator


@allure.epic("云医疗系统")
@allure.feature("药物管理")
class TestMedicineAPI:
    """药物管理API测试类"""
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_medicines_success(self, http_client: HTTPClient):
        """测试获取药物列表的正常功能"""
        with allure.step("发送获取药物列表请求"):
            response = http_client.get("/api/medicines")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 5.0)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 关键词筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_get_medicines_with_keyword(self, http_client: HTTPClient):
        """测试通过关键词筛选药物列表"""
        test_keyword = "阿莫西林"
        
        with allure.step(f"发送带关键词'{test_keyword}'的请求"):
            response = http_client.get("/api/medicines", params={"keyword": test_keyword})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的药物名称包含关键词（如果有数据的话）
            json_data = response.json()
            if json_data['total'] > 0:
                medicines = json_data['data']
                for medicine in medicines:
                    assert test_keyword.lower() in medicine.get('name', '').lower() or \
                           test_keyword.lower() in medicine.get('manufacturer', '').lower() or \
                           test_keyword.lower() in medicine.get('description', '').lower()
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 分类筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_get_medicines_with_category(self, http_client: HTTPClient):
        """测试通过分类筛选药物列表"""
        test_category = "抗生素"
        
        with allure.step(f"发送带分类'{test_category}'的请求"):
            response = http_client.get("/api/medicines", params={"category": test_category})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取药物分类")
    @allure.title("获取药物分类列表 - 正常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_medicine_categories_success(self, http_client: HTTPClient):
        """测试获取药物分类列表的正常功能"""
        with allure.step("发送获取药物分类请求"):
            response = http_client.get("/api/medicines/categories")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 3.0)
            assert_helper.assert_json_structure(response, ['code', 'data'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 无效关键词")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.negative
    def test_get_medicines_with_invalid_keyword(self, http_client: HTTPClient):
        """测试使用不存在的关键词筛选药物"""
        invalid_keyword = "不存在的药物名称12345"
        
        with allure.step(f"发送带无效关键词'{invalid_keyword}'的请求"):
            response = http_client.get("/api/medicines", params={"keyword": invalid_keyword})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            assert_helper.assert_json_value(response, 'total', 0)
            
            # 验证返回空列表
            json_data = response.json()
            assert len(json_data['data']) == 0
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 特殊字符关键词")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.boundary
    def test_get_medicines_with_special_characters(self, http_client: HTTPClient):
        """测试使用特殊字符作为关键词筛选药物"""
        special_keyword = "!@#$%^&*()"
        
        with allure.step(f"发送带特殊字符关键词'{special_keyword}'的请求"):
            response = http_client.get("/api/medicines", params={"keyword": special_keyword})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 空关键词")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.boundary
    def test_get_medicines_with_empty_keyword(self, http_client: HTTPClient):
        """测试使用空关键词筛选药物"""
        with allure.step("发送带空关键词的请求"):
            response = http_client.get("/api/medicines", params={"keyword": ""})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 长关键词")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.boundary
    def test_get_medicines_with_long_keyword(self, http_client: HTTPClient):
        """测试使用超长关键词筛选药物"""
        long_keyword = "a" * 1000  # 1000个字符的关键词
        
        with allure.step(f"发送带超长关键词的请求（{len(long_keyword)}个字符）"):
            response = http_client.get("/api/medicines", params={"keyword": long_keyword})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取药物列表")
    @allure.title("获取药物列表 - 多参数组合")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_medicines_with_multiple_params(self, http_client: HTTPClient):
        """测试同时使用关键词和分类筛选药物"""
        params = {
            "keyword": "阿莫西林",
            "category": "抗生素"
        }
        
        with allure.step("发送带多个筛选参数的请求"):
            response = http_client.get("/api/medicines", params=params)
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("性能测试")
    @allure.title("获取药物列表 - 响应时间测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_medicines_performance(self, http_client: HTTPClient):
        """测试获取药物列表的性能"""
        with allure.step("发送性能测试请求"):
            response = http_client.get("/api/medicines")
        
        with allure.step("验证响应时间"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 2.0)  # 要求2秒内响应
            
            # 记录实际响应时间
            actual_time = response.elapsed.total_seconds()
            allure.attach(
                f"{actual_time:.3f}秒",
                name="实际响应时间",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story("新增药品")
    @allure.title("新增一个药品")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_create_medicine(self, http_client: HTTPClient):
        """测试新增一个药品"""
        with allure.step("发送post请求"):
            new_medicine = data_generator.generate_medicine_data(name="测试药品")
            response = http_client.post("/api/medicines", json_data=new_medicine)

        with allure.step("基础断言验证"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'message', 'data'])
            assert_helper.assert_json_value(response, 'code', 0)
            assert_helper.assert_json_contains(response, 'message', "成功")

            json_data = response.json()
            medicine_data = json_data['data']
        
        with allure.step("data断言验证"):
            if medicine_data:
                assert 'id' in medicine_data
                assert_helper.assert_json_value(response, 'data.name', new_medicine['name'])

            
        
