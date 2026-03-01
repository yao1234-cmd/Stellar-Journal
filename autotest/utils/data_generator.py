# -*- coding: utf-8 -*-
"""
测试数据生成器 - 生成各种测试数据
"""

import json
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List
from faker import Faker


class DataGenerator:
    """测试数据生成器"""
    
    def __init__(self, locale='zh_CN'):
        """
        初始化数据生成器
        
        Args:
            locale: 本地化设置
        """
        self.fake = Faker(locale)
    
    def generate_medicine_data(self, **overrides) -> Dict[str, Any]:
        """
        生成药物数据
        
        Args:
            **overrides: 覆盖字段
            
        Returns:
            药物数据字典
        """
        categories = ['抗生素', '感冒药', '止痛药', '消炎药', '维生素', '中成药']
        manufacturers = ['华北制药', '同仁堂', '云南白药', '哈药集团', '石药集团']
        
        data = {
            'name': f"{self.fake.word()}胶囊",
            'category': random.choice(categories),
            'specification': f"{random.randint(10, 500)}mg*{random.randint(10, 100)}粒",
            'manufacturer': random.choice(manufacturers),
            'price': round(random.uniform(5.0, 200.0), 2),
            'stock': random.randint(0, 1000),
            'description': self.fake.text(max_nb_chars=100)
        }
        
        data.update(overrides)
        return data
    
    def generate_patient_data(self, **overrides) -> Dict[str, Any]:
        """
        生成患者数据
        
        Args:
            **overrides: 覆盖字段
            
        Returns:
            患者数据字典
        """
        data = {
            'patient_name': self.fake.name(),
            'gender': random.choice(['男', '女']),
            'age': random.randint(1, 100),
            'phone': self.fake.phone_number(),
            'id_card': self.fake.ssn(),
            'address': self.fake.address(),
            'medical_history': self.fake.text(max_nb_chars=200)
        }
        
        data.update(overrides)
        return data
    
    def generate_doctor_data(self, **overrides) -> Dict[str, Any]:
        """
        生成医生数据
        
        Args:
            **overrides: 覆盖字段
            
        Returns:
            医生数据字典
        """
        departments = ['内科', '外科', '儿科', '妇产科', '眼科', '耳鼻喉科', '皮肤科', '骨科']
        titles = ['主任医师', '副主任医师', '主治医师', '住院医师']
        specializations = ['心血管疾病', '消化系统疾病', '呼吸系统疾病', '神经系统疾病']
        
        data = {
            'doctor_name': f"Dr. {self.fake.name()}",
            'gender': random.choice(['男', '女']),
            'department': random.choice(departments),
            'title': random.choice(titles),
            'phone': self.fake.phone_number(),
            'email': self.fake.email(),
            'specialization': random.choice(specializations),
            'years_of_experience': random.randint(1, 30),
            'status': random.choice(['在职', '休假', '离职'])
        }
        
        data.update(overrides)
        return data
    
    def generate_consultation_data(self, **overrides) -> Dict[str, Any]:
        """
        生成就诊数据
        
        Args:
            **overrides: 覆盖字段
            
        Returns:
            就诊数据字典
        """
        departments = ['内科', '外科', '儿科', '妇产科', '眼科']
        statuses = ['待就诊', '就诊中', '已完成', '已取消']
        
        data = {
            'patient_id': random.randint(1, 100),
            'patient_name': self.fake.name(),
            'doctor_name': f"Dr. {self.fake.name()}",
            'department': random.choice(departments),
            'diagnosis': self.fake.text(max_nb_chars=100),
            'prescription': self.fake.text(max_nb_chars=200),
            'status': random.choice(statuses),
            'consultation_date': self.fake.date()
        }
        
        data.update(overrides)
        return data
    
    def generate_appointment_data(self, **overrides) -> Dict[str, Any]:
        """
        生成预约数据
        
        Args:
            **overrides: 覆盖字段
            
        Returns:
            预约数据字典
        """
        departments = ['内科', '外科', '儿科', '妇产科', '眼科']
        statuses = ['待确认', '已确认', '已完成', '已取消']
        times = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
        
        data = {
            'patient_id': random.randint(1, 100),
            'patient_name': self.fake.name(),
            'doctor_id': random.randint(1, 50),
            'doctor_name': f"Dr. {self.fake.name()}",
            'department': random.choice(departments),
            'appointment_date': (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'appointment_time': random.choice(times),
            'reason': self.fake.text(max_nb_chars=100),
            'status': random.choice(statuses),
            'notes': self.fake.text(max_nb_chars=150)
        }
        
        data.update(overrides)
        return data
    
    def generate_invalid_data(self, data_type: str) -> Dict[str, Any]:
        """
        生成无效数据用于负向测试
        
        Args:
            data_type: 数据类型
            
        Returns:
            无效数据字典
        """
        invalid_data_map = {
            'medicine': {
                'name': '',  # 空名称
                'price': -10,  # 负价格
                'stock': -5,   # 负库存
            },
            'patient': {
                'patient_name': '',  # 空姓名
                'age': -1,          # 负年龄
                'phone': '123',     # 无效手机号
            },
            'doctor': {
                'doctor_name': '',           # 空姓名
                'years_of_experience': -1,   # 负经验年数
                'email': 'invalid_email',    # 无效邮箱
            }
        }
        
        return invalid_data_map.get(data_type, {})
    
    def generate_boundary_data(self, field: str, data_type: str) -> List[Any]:
        """
        生成边界测试数据
        
        Args:
            field: 字段名
            data_type: 数据类型
            
        Returns:
            边界值列表
        """
        boundary_map = {
            'string': {
                'name': ['', 'a', 'a' * 50, 'a' * 255, 'a' * 256],
                'phone': ['', '1', '13800138000', '1380013800012345'],
            },
            'integer': {
                'age': [0, 1, 150, 151],
                'stock': [0, 1, 9999, 10000],
                'price': [0, 0.01, 9999.99, 10000],
            }
        }
        
        return boundary_map.get(data_type, {}).get(field, [])


# 全局数据生成器实例
data_generator = DataGenerator()