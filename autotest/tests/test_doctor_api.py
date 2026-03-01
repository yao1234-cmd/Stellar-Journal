# -*- coding: utf-8 -*-
"""
医生管理API测试用例
"""

import json
from urllib import response
import pytest
import allure
from utils.http_client import HTTPClient
from utils.assertion_helper import assert_helper


@allure.epic("云医疗系统")
@allure.feature("医生管理")
class TestDoctorAPI:
    """医生管理API测试类"""
    
    @allure.story("获取医生列表")
    @allure.title("获取医生列表 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_doctors_success(self, http_client: HTTPClient):
        """测试获取医生列表的正常功能"""
        with allure.step("发送获取医生列表请求"):
            response = http_client.get("/api/doctors")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 5.0)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取医生列表")
    @allure.title("按科室筛选医生")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("department", ["内科", "外科", "儿科", "妇产科", "眼科", "耳鼻喉科"])
    def test_get_doctors_by_department(self, http_client: HTTPClient, department):
        """测试按科室筛选医生"""
        with allure.step(f"发送按科室'{department}'筛选的请求"):
            response = http_client.get("/api/doctors", params={"department": department})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的医生科室正确
            json_data = response.json()
            doctors = json_data['data']
            
            for doctor in doctors:
                assert doctor.get('department') == department, f"医生科室应为{department}"
    
    @allure.story("获取医生列表")
    @allure.title("按状态筛选医生")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("status", ["在职", "休假", "离职"])
    def test_get_doctors_by_status(self, http_client: HTTPClient, status):
        """测试按状态筛选医生"""
        with allure.step(f"发送按状态'{status}'筛选的请求"):
            response = http_client.get("/api/doctors", params={"status": status})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的医生状态正确
            json_data = response.json()
            doctors = json_data['data']
            
            for doctor in doctors:
                assert doctor.get('status') == status, f"医生状态应为{status}"
    
    @allure.story("获取医生详情")
    @allure.title("获取医生详情 - 正常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_doctor_detail_success(self, http_client: HTTPClient):
        """测试获取医生详情的正常功能"""
        doctor_id = 1
        
        with allure.step(f"发送获取医生详情请求 (ID: {doctor_id})"):
            response = http_client.get(f"/api/doctors/{doctor_id}")
        
        with allure.step("验证响应"):
            # 可能返回404（记录不存在）或200（记录存在）
            if response.status_code == 200:
                assert_helper.assert_json_structure(response, ['code', 'data'])
                assert_helper.assert_json_value(response, 'code', 0)
                
                # 验证医生记录字段
                json_data = response.json()
                doctor = json_data['data']
                expected_fields = ['id', 'doctor_name', 'department', 'title', 'status']
                
                for field in expected_fields:
                    assert field in doctor, f"医生记录应包含{field}字段"
            elif response.status_code == 404:
                assert_helper.assert_json_structure(response, ['detail'])
            else:
                pytest.fail(f"意外的状态码: {response.status_code}")
    
    @allure.story("获取医生详情")
    @allure.title("获取不存在的医生详情")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_doctor_detail_not_found(self, http_client: HTTPClient):
        """测试获取不存在的医生详情"""
        non_existent_id = 99999
        
        with allure.step(f"发送获取不存在医生详情请求 (ID: {non_existent_id})"):
            response = http_client.get(f"/api/doctors/{non_existent_id}")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 404)
            assert_helper.assert_json_structure(response, ['detail'])
    
    @allure.story("更新医生状态")
    @allure.title("更新医生状态 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("new_status", ["在职", "休假", "离职"])
    def test_update_doctor_status_success(self, http_client: HTTPClient, new_status):
        """测试更新医生状态的正常功能"""
        doctor_id = 1
        
        with allure.step(f"发送更新医生状态请求 (ID: {doctor_id}, 状态: {new_status})"):
            response = http_client.put(
                f"/api/doctors/{doctor_id}/status",
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
    
    @allure.story("获取科室列表")
    @allure.title("获取医生科室列表 - 正常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_doctor_departments_success(self, http_client: HTTPClient):
        """测试获取医生科室列表的正常功能"""
        with allure.step("发送获取科室列表请求"):
            response = http_client.get("/api/doctors/departments/list")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 3.0)
            assert_helper.assert_json_structure(response, ['code', 'data'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证科室列表是数组
            json_data = response.json()
            departments = json_data['data']
            assert isinstance(departments, list), "科室列表应为数组类型"
            
            # 如果有科室数据，验证每个科室都是字符串
            for department in departments:
                assert isinstance(department, str), "科室名称应为字符串类型"
                assert len(department) > 0, "科室名称不应为空"
    
    @allure.story("数据验证")
    @allure.title("医生记录数据结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_doctor_data_structure(self, http_client: HTTPClient):
        """测试医生记录数据结构的完整性"""
        with allure.step("发送获取医生列表请求"):
            response = http_client.get("/api/doctors")
        
        with allure.step("验证数据结构"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            doctors = json_data['data']
            
            # 如果有医生记录，验证数据结构
            if len(doctors) > 0:
                doctor = doctors[0]
                expected_fields = [
                    'id', 'doctor_name', 'gender', 'department', 'title',
                    'phone', 'email', 'specialization', 'years_of_experience', 'status'
                ]
                
                for field in expected_fields:
                    if field in doctor:
                        # 验证字段类型
                        if field in ['id', 'years_of_experience']:
                            assert isinstance(doctor[field], int), f"{field}应为整数类型"
                        elif field in ['doctor_name', 'gender', 'department', 'title', 'phone', 'email', 'specialization', 'status']:
                            assert isinstance(doctor[field], str), f"{field}应为字符串类型"
                        
                        # 验证特定字段的值范围
                        if field == 'gender' and doctor[field]:
                            assert doctor[field] in ['男', '女'], "性别值应为'男'或'女'"
                        
                        if field == 'years_of_experience' and doctor[field] is not None:
                            assert doctor[field] >= 0, "工作经验年数应为非负数"
                        
                        if field == 'status':
                            assert doctor[field] in ['在职', '休假', '离职'], "状态值应为有效状态"
    
    @allure.story("边界测试")
    @allure.title("获取医生详情 - 无效ID格式")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.boundary
    @pytest.mark.parametrize("invalid_id", ["abc", "0", "-1", "999999999999999999999"])
    def test_get_doctor_detail_invalid_id(self, http_client: HTTPClient, invalid_id):
        """测试使用无效ID格式获取医生详情"""
        with allure.step(f"发送无效ID请求 (ID: {invalid_id})"):
            response = http_client.get(f"/api/doctors/{invalid_id}")
        
        with allure.step("验证响应"):
            # 可能返回404、422或其他错误状态码
            assert response.status_code in [404, 422, 400], "应该返回错误状态码"
    
    @allure.story("组合筛选")
    @allure.title("医生列表 - 多条件筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_doctors_multiple_filters(self, http_client: HTTPClient):
        """测试同时使用多个条件筛选医生"""
        params = {
            "department": "内科",
            "status": "在职"
        }
        
        with allure.step("发送多条件筛选请求"):
            response = http_client.get("/api/doctors", params=params)
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的医生同时满足两个条件
            json_data = response.json()
            doctors = json_data['data']
            
            for doctor in doctors:
                assert doctor.get('department') == params['department'], f"科室应为{params['department']}"
                assert doctor.get('status') == params['status'], f"状态应为{params['status']}"
    
    @allure.story("性能测试")
    @allure.title("获取医生列表 - 响应时间测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_doctors_performance(self, http_client: HTTPClient):
        """测试获取医生列表的性能"""
        with allure.step("发送性能测试请求"):
            response = http_client.get("/api/doctors")
        
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
    
    @allure.story("排序验证")
    @allure.title("医生列表排序验证")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.positive
    def test_doctors_list_sorting(self, http_client: HTTPClient):
        """测试医生列表的排序功能"""
        with allure.step("发送获取医生列表请求"):
            response = http_client.get("/api/doctors")
        
        with allure.step("验证排序"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            doctors = json_data['data']
            
            # 验证按ID倒序排序（根据API文档）
            if len(doctors) > 1:
                ids = [doctor.get('id', 0) for doctor in doctors]
                assert ids == sorted(ids, reverse=True), "医生列表应按ID倒序排列"


    @allure.story("数据验证")
    @allure.title("医生列表 total 字段与返回数量一致")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_dovtors_total_matches(self, http_client: HTTPClient):
        """医生列表 total 字段应与 data 列表长度一致"""
        with allure.step("发送获取医生列表请求"):
            response = http_client.get("/api/doctors")

        with allure.step("验证基础响应信息"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code','data','total'])
            assert_helper.assert_json_value(response, 'code', 0)

        with allure.step("验证 total 与 data 长度一致"):
            json_data = response.json()
            doctors = json_data['data']
            total = json_data['total']
            assert total == len(doctors), f"total={total} 应等于 列表长度={len(doctors)}"


    @allure.story("数据验证")
    @allure.title("验证医生状态")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_doctor_status_matches(self, http_client: HTTPClient):
        """验证筛选后的医生状态是否和筛选条件一致"""
        with allure.step("发送http请求"):
            response = http_client.get("/api/doctors", params={"status": "在职"})

        with allure.step("基础验证"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code','data','total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            json_data = response.json()
            doctors = json_data['data']

        with allure.step("验证返回医生状态与筛选条件一致"):
            if doctors:
                for doctor in doctors:
                    assert doctor['status'] == "在职", f"期望医生状态为'在职'，实际为: {doctor.get('status')}"
