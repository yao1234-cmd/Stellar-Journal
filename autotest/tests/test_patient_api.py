# -*- coding: utf-8 -*-
"""
患者管理API测试用例
"""

import pytest
import allure
from utils.http_client import HTTPClient
from utils.assertion_helper import assert_helper


@allure.epic("云医疗系统")
@allure.feature("患者管理")
class TestPatientAPI:
    """患者管理API测试类"""
    
    @allure.story("患者统计")
    @allure.title("获取患者统计数据 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_patient_stats_success(self, http_client: HTTPClient):
        """测试获取患者统计数据的正常功能"""
        with allure.step("发送获取患者统计请求"):
            response = http_client.get("/api/patients/stats")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 5.0)
            assert_helper.assert_json_structure(response, ['code', 'data'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证统计数据结构
            expected_stats_keys = [
                'total_patients',
                'today_consultations', 
                'pending_consultations',
                'ongoing_consultations',
                'gender_stats',
                'department_stats',
                'trend_data'
            ]
            
            json_data = response.json()
            stats_data = json_data['data']
            
            for key in expected_stats_keys:
                assert key in stats_data, f"统计数据缺少字段: {key}"
    
    @allure.story("患者统计")
    @allure.title("验证患者统计数据类型")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_patient_stats_data_types(self, http_client: HTTPClient):
        """测试患者统计数据的数据类型"""
        with allure.step("发送获取患者统计请求"):
            response = http_client.get("/api/patients/stats")
        
        with allure.step("验证数据类型"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            stats_data = json_data['data']
            
            # 验证数值类型字段
            numeric_fields = [
                'total_patients',
                'today_consultations',
                'pending_consultations', 
                'ongoing_consultations'
            ]
            
            for field in numeric_fields:
                assert isinstance(stats_data[field], int), f"{field} 应该是整数类型"
                assert stats_data[field] >= 0, f"{field} 应该是非负数"
            
            # 验证数组类型字段
            array_fields = ['gender_stats', 'department_stats', 'trend_data']
            
            for field in array_fields:
                assert isinstance(stats_data[field], list), f"{field} 应该是数组类型"
    
    @allure.story("患者统计")
    @allure.title("验证性别统计数据结构")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_gender_stats_structure(self, http_client: HTTPClient):
        """测试性别统计数据的结构"""
        with allure.step("发送获取患者统计请求"):
            response = http_client.get("/api/patients/stats")
        
        with allure.step("验证性别统计数据结构"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            gender_stats = json_data['data']['gender_stats']
            
            # 如果有性别统计数据，验证结构
            if len(gender_stats) > 0:
                for gender_stat in gender_stats:
                    assert 'gender' in gender_stat, "性别统计应包含gender字段"
                    assert 'count' in gender_stat, "性别统计应包含count字段"
                    assert gender_stat['gender'] in ['男', '女'], "性别值应为'男'或'女'"
                    assert isinstance(gender_stat['count'], int), "count应为整数"
                    assert gender_stat['count'] >= 0, "count应为非负数"
    
    @allure.story("患者统计")
    @allure.title("验证科室统计数据结构")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_department_stats_structure(self, http_client: HTTPClient):
        """测试科室统计数据的结构"""
        with allure.step("发送获取患者统计请求"):
            response = http_client.get("/api/patients/stats")
        
        with allure.step("验证科室统计数据结构"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            department_stats = json_data['data']['department_stats']
            
            # 如果有科室统计数据，验证结构
            if len(department_stats) > 0:
                for dept_stat in department_stats:
                    assert 'department' in dept_stat, "科室统计应包含department字段"
                    assert 'count' in dept_stat, "科室统计应包含count字段"
                    assert isinstance(dept_stat['department'], str), "department应为字符串"
                    assert isinstance(dept_stat['count'], int), "count应为整数"
                    assert dept_stat['count'] >= 0, "count应为非负数"
                
                # 验证按数量降序排列
                counts = [stat['count'] for stat in department_stats]
                assert counts == sorted(counts, reverse=True), "科室统计应按数量降序排列"
    
    @allure.story("患者统计")
    @allure.title("验证趋势数据结构")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_trend_data_structure(self, http_client: HTTPClient):
        """测试趋势数据的结构"""
        with allure.step("发送获取患者统计请求"):
            response = http_client.get("/api/patients/stats")
        
        with allure.step("验证趋势数据结构"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            trend_data = json_data['data']['trend_data']
            
            # 如果有趋势数据，验证结构
            if len(trend_data) > 0:
                for trend_item in trend_data:
                    assert 'date' in trend_item, "趋势数据应包含date字段"
                    assert 'count' in trend_item, "趋势数据应包含count字段"
                    assert isinstance(trend_item['date'], str), "date应为字符串"
                    assert isinstance(trend_item['count'], int), "count应为整数"
                    assert trend_item['count'] >= 0, "count应为非负数"
                    
                    # 验证日期格式（YYYY-MM-DD）
                    import re
                    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                    assert re.match(date_pattern, trend_item['date']), f"日期格式错误: {trend_item['date']}"
    
    @allure.story("患者统计")
    @allure.title("患者统计数据一致性验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_patient_stats_consistency(self, http_client: HTTPClient):
        """测试患者统计数据的一致性"""
        with allure.step("发送获取患者统计请求"):
            response = http_client.get("/api/patients/stats")
        
        with allure.step("验证数据一致性"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            stats_data = json_data['data']
            
            # 验证性别统计总数不超过总患者数
            gender_stats = stats_data['gender_stats']
            total_patients = stats_data['total_patients']
            
            if len(gender_stats) > 0:
                gender_total = sum(stat['count'] for stat in gender_stats)
                assert gender_total <= total_patients, "性别统计总数不应超过总患者数"
            
            # 验证今日就诊数不超过总患者数
            today_consultations = stats_data['today_consultations']
            assert today_consultations <= total_patients, "今日就诊数不应超过总患者数"
            
            # 验证待就诊和就诊中数量的合理性
            pending_consultations = stats_data['pending_consultations']
            ongoing_consultations = stats_data['ongoing_consultations']
            
            assert pending_consultations >= 0, "待就诊数不应为负数"
            assert ongoing_consultations >= 0, "就诊中数不应为负数"
    
    @allure.story("性能测试")
    @allure.title("患者统计 - 响应时间测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_patient_stats_performance(self, http_client: HTTPClient):
        """测试获取患者统计的性能"""
        with allure.step("发送性能测试请求"):
            response = http_client.get("/api/patients/stats")
        
        with allure.step("验证响应时间"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 3.0)  # 要求3秒内响应
            
            # 记录实际响应时间
            actual_time = response.elapsed.total_seconds()
            allure.attach(
                f"{actual_time:.3f}秒",
                name="实际响应时间",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.story("边界测试")
    @allure.title("患者统计 - 并发请求测试")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.boundary
    def test_patient_stats_concurrent_requests(self, http_client: HTTPClient):
        """测试患者统计接口的并发处理能力"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = http_client.get("/api/patients/stats")
            results.append(response.status_code)
        
        with allure.step("发送并发请求"):
            threads = []
            for i in range(5):  # 创建5个并发请求
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()
            
            # 等待所有线程完成
            for thread in threads:
                thread.join()
        
        with allure.step("验证并发请求结果"):
            assert len(results) == 5, "应该收到5个响应"
            assert all(status == 200 for status in results), "所有请求都应该成功"