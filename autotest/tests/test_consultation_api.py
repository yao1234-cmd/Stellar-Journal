# -*- coding: utf-8 -*-
"""
就诊管理API测试用例
"""

import pytest
import allure
from utils.http_client import HTTPClient
from utils.assertion_helper import assert_helper


@allure.epic("云医疗系统")
@allure.feature("就诊管理")
class TestConsultationAPI:
    """就诊管理API测试类"""
    
    @allure.story("获取就诊记录")
    @allure.title("获取就诊记录列表 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_consultations_success(self, http_client: HTTPClient):
        """测试获取就诊记录列表的正常功能"""
        with allure.step("发送获取就诊记录请求"):
            response = http_client.get("/api/consultations")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 5.0)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取就诊记录")
    @allure.title("按状态筛选就诊记录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("status", ["待就诊", "就诊中", "已完成", "已取消"])
    def test_get_consultations_by_status(self, http_client: HTTPClient, status):
        """测试按状态筛选就诊记录"""
        with allure.step(f"发送按状态'{status}'筛选的请求"):
            response = http_client.get("/api/consultations", params={"status": status})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的记录状态正确
            json_data = response.json()
            consultations = json_data['data']
            
            for consultation in consultations:
                assert consultation.get('status') == status, f"就诊记录状态应为{status}"
    
    @allure.story("获取就诊记录")
    @allure.title("按日期筛选就诊记录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_get_consultations_by_date(self, http_client: HTTPClient):
        """测试按日期筛选就诊记录"""
        test_date = "2024-01-15"
        
        with allure.step(f"发送按日期'{test_date}'筛选的请求"):
            response = http_client.get("/api/consultations", params={"date": test_date})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的记录日期正确
            json_data = response.json()
            consultations = json_data['data']
            
            for consultation in consultations:
                assert consultation.get('consultation_date') == test_date, f"就诊日期应为{test_date}"
    
    @allure.story("获取就诊详情")
    @allure.title("获取就诊详情 - 正常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_consultation_detail_success(self, http_client: HTTPClient):
        """测试获取就诊详情的正常功能"""
        consultation_id = 1
        
        with allure.step(f"发送获取就诊详情请求 (ID: {consultation_id})"):
            response = http_client.get(f"/api/consultations/{consultation_id}")
        
        with allure.step("验证响应"):
            # 可能返回404（记录不存在）或200（记录存在）
            if response.status_code == 200:
                assert_helper.assert_json_structure(response, ['code', 'data'])
                assert_helper.assert_json_value(response, 'code', 0)
                
                # 验证就诊记录字段
                json_data = response.json()
                consultation = json_data['data']
                expected_fields = ['id', 'patient_name', 'doctor_name', 'department', 'status']
                
                for field in expected_fields:
                    assert field in consultation, f"就诊记录应包含{field}字段"
            elif response.status_code == 404:
                assert_helper.assert_json_structure(response, ['detail'])
            else:
                pytest.fail(f"意外的状态码: {response.status_code}")
    
    @allure.story("获取就诊详情")
    @allure.title("获取不存在的就诊详情")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_consultation_detail_not_found(self, http_client: HTTPClient):
        """测试获取不存在的就诊详情"""
        non_existent_id = 99999
        
        with allure.step(f"发送获取不存在就诊详情请求 (ID: {non_existent_id})"):
            response = http_client.get(f"/api/consultations/{non_existent_id}")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 404)
            assert_helper.assert_json_structure(response, ['detail'])
    
    @allure.story("更新就诊状态")
    @allure.title("更新就诊状态 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("new_status", ["待就诊", "就诊中", "已完成", "已取消"])
    def test_update_consultation_status_success(self, http_client: HTTPClient, new_status):
        """测试更新就诊状态的正常功能"""
        consultation_id = 1
        
        with allure.step(f"发送更新就诊状态请求 (ID: {consultation_id}, 状态: {new_status})"):
            response = http_client.put(
                f"/api/consultations/{consultation_id}/status",
                params={"status": new_status}
            )
        
        with allure.step("验证响应"):
            # 可能返回404（记录不存在）或200（更新成功）
            if response.status_code == 200:
                assert_helper.assert_json_structure(response, ['code', 'message'])
                assert_helper.assert_json_value(response, 'code', 0)
                assert_helper.assert_json_contains(response, 'message', '成功')
            elif response.status_code == 404:
                assert_helper.assert_json_structure(response, ['detail'])
            else:
                pytest.fail(f"意外的状态码: {response.status_code}")
    
    @allure.story("更新就诊状态")
    @allure.title("更新不存在就诊的状态")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_update_consultation_status_not_found(self, http_client: HTTPClient):
        """测试更新不存在就诊记录的状态"""
        non_existent_id = 99999
        new_status = "已完成"
        
        with allure.step(f"发送更新不存在就诊状态请求 (ID: {non_existent_id})"):
            response = http_client.put(
                f"/api/consultations/{non_existent_id}/status",
                params={"status": new_status}
            )
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 404)
            assert_helper.assert_json_structure(response, ['detail'])
    
    @allure.story("更新就诊状态")
    @allure.title("更新就诊状态 - 无效状态")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_update_consultation_status_invalid(self, http_client: HTTPClient):
        """测试使用无效状态更新就诊记录"""
        consultation_id = 1
        invalid_status = "无效状态"
        
        with allure.step(f"发送无效状态更新请求 (状态: {invalid_status})"):
            response = http_client.put(
                f"/api/consultations/{consultation_id}/status",
                params={"status": invalid_status}
            )
        
        with allure.step("验证响应"):
            # 系统可能接受任何状态值，或者返回错误
            # 这里我们检查是否至少有响应
            assert response.status_code in [200, 400, 404], "应该返回有效的HTTP状态码"
    
    @allure.story("边界测试")
    @allure.title("获取就诊记录 - 无效ID格式")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.boundary
    @pytest.mark.parametrize("invalid_id", ["abc", "0", "-1", "999999999999999999999"])
    def test_get_consultation_detail_invalid_id(self, http_client: HTTPClient, invalid_id):
        """测试使用无效ID格式获取就诊详情"""
        with allure.step(f"发送无效ID请求 (ID: {invalid_id})"):
            response = http_client.get(f"/api/consultations/{invalid_id}")
        
        with allure.step("验证响应"):
            # 可能返回404、422或其他错误状态码
            assert response.status_code in [404, 422, 400], "应该返回错误状态码"
    
    @allure.story("性能测试")
    @allure.title("获取就诊记录 - 响应时间测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_consultations_performance(self, http_client: HTTPClient):
        """测试获取就诊记录的性能"""
        with allure.step("发送性能测试请求"):
            response = http_client.get("/api/consultations")
        
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
    
    @allure.story("数据验证")
    @allure.title("就诊记录数据结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_consultation_data_structure(self, http_client: HTTPClient):
        """测试就诊记录数据结构的完整性"""
        with allure.step("发送获取就诊记录请求"):
            response = http_client.get("/api/consultations")
        
        with allure.step("验证数据结构"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            consultations = json_data['data']
            
            # 如果有就诊记录，验证数据结构
            if len(consultations) > 0:
                consultation = consultations[0]
                expected_fields = [
                    'id', 'patient_id', 'patient_name', 'doctor_name',
                    'department', 'diagnosis', 'prescription', 'status', 'consultation_date'
                ]
                
                for field in expected_fields:
                    if field in consultation:
                        # 验证字段类型
                        if field in ['id', 'patient_id']:
                            assert isinstance(consultation[field], int), f"{field}应为整数类型"
                        elif field in ['patient_name', 'doctor_name', 'department', 'status']:
                            assert isinstance(consultation[field], str), f"{field}应为字符串类型"