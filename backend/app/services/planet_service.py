"""
Planet Service - 星球状态计算服务
"""
from typing import List, Dict
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.record import Record, RecordType
import random
import math


class PlanetService:
    """星球服务"""
    
    def calculate_star_position(self, index: int, total: int, record_date: datetime) -> Dict:
        """
        计算星星的3D位置（轨道参数）
        
        Args:
            index: 星星索引
            total: 总星星数
            record_date: 记录日期
            
        Returns:
            {"orbit_radius": 2.0, "orbit_angle": 45, "x": 0, "y": 0, "z": 2}
        """
        # 使用日期作为随机种子，确保同一天的星星位置稳定
        seed = int(record_date.timestamp()) + index
        random.seed(seed)
        
        # 轨道半径：1.5 - 3.0
        orbit_radius = 1.5 + random.random() * 1.5
        
        # 轨道角度：均匀分布
        orbit_angle = (360 / max(total, 1) * index + random.random() * 30) % 360
        
        # 计算笛卡尔坐标
        angle_rad = math.radians(orbit_angle)
        x = orbit_radius * math.cos(angle_rad)
        y = random.random() * 0.5 - 0.25  # 轻微上下浮动
        z = orbit_radius * math.sin(angle_rad)
        
        return {
            "orbit_radius": round(orbit_radius, 2),
            "orbit_angle": round(orbit_angle, 2),
            "x": round(x, 2),
            "y": round(y, 2),
            "z": round(z, 2)
        }
    
    def calculate_tree_position(self, theme: str, index: int) -> Dict:
        """
        计算树木的位置（在星球表面）
        
        Args:
            theme: 主题名称
            index: 同主题的索引
            
        Returns:
            {"x": 0.5, "y": 0.0, "z": 0.8}
        """
        # 使用主题名称作为随机种子
        seed = hash(theme) + index
        random.seed(seed)
        
        # 在球面上均匀分布
        theta = random.random() * 2 * math.pi
        phi = math.acos(2 * random.random() - 1)
        
        # 球面坐标转笛卡尔坐标（半径=1，表面）
        x = math.sin(phi) * math.cos(theta)
        y = math.sin(phi) * math.sin(theta)
        z = math.cos(phi)
        
        return {
            "x": round(x, 2),
            "y": round(y, 2),
            "z": round(z, 2)
        }
    
    async def get_planet_state(self, db: Session, user_id: str, target_date: date = None) -> Dict:
        """
        获取星球当前状态
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            target_date: 目标日期，默认今天
            
        Returns:
            星球状态数据
        """
        if target_date is None:
            target_date = date.today()
        
        # 查询当日所有记录
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        records = db.query(Record).filter(
            and_(
                Record.user_id == user_id,
                Record.created_at >= start_datetime,
                Record.created_at <= end_datetime
            )
        ).order_by(Record.created_at).all()
        
        # 计算大气层颜色（当日心情综合）
        mood_records = [r for r in records if r.type == RecordType.MOOD]
        atmosphere_color = "#87CEEB"  # 默认天蓝色
        
        if mood_records and mood_records[-1].color_hex:
            # 使用最新的心情颜色
            atmosphere_color = mood_records[-1].color_hex
        
        # 收集星星（灵感）
        spark_records = [r for r in records if r.type == RecordType.SPARK]
        stars = []
        for idx, record in enumerate(spark_records):
            stars.append({
                "id": str(record.id),
                "position": record.position_data or {},
                "color": "#FFD700",  # 金黄色
                "size": 0.1,
                "keyword": record.keywords[0] if record.keywords else "灵感"
            })
        
        # 收集树木（思考）- 按主题聚类
        thought_records = [r for r in records if r.type == RecordType.THOUGHT]
        theme_groups = {}
        for record in thought_records:
            theme = record.theme_cluster or "未分类"
            if theme not in theme_groups:
                theme_groups[theme] = []
            theme_groups[theme].append(record)
        
        trees = []
        for theme, group in theme_groups.items():
            # 树的大小基于该主题下的记录数量
            size = 0.3 + min(len(group) * 0.1, 0.7)
            trees.append({
                "id": f"tree-{theme}",
                "position": group[0].position_data or {},
                "theme": theme,
                "leaf_count": len(group),
                "size": size
            })
        
        return {
            "date": target_date.isoformat(),
            "atmosphere_color": atmosphere_color,
            "stars": stars,
            "trees": trees,
            "total_records": len(records)
        }
    
    async def get_planet_history(
        self, 
        db: Session, 
        user_id: str, 
        days: int = 30
    ) -> List[Dict]:
        """
        获取星球历史
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        # 1. 一次性查询时间范围内的所有心情记录
        mood_records = db.query(
            func.date(Record.created_at).label('date'),
            Record.color_hex
        ).filter(
            Record.user_id == user_id,
            Record.type == RecordType.MOOD,
            Record.created_at >= start_datetime,
            Record.created_at <= end_datetime
        ).order_by(Record.created_at.desc()).all()
        
        # 构建心情字典：日期 -> 最新颜色
        mood_map = {}
        for r in mood_records:
            # 由于是倒序排列，只有第一次遇到的日期（最新的）会被记录
            d_str = r.date.isoformat() if hasattr(r.date, 'isoformat') else str(r.date)
            if d_str not in mood_map:
                mood_map[d_str] = r.color_hex

        # 2. 一次性查询每日记录总数
        daily_counts = db.query(
            func.date(Record.created_at).label('date'),
            func.count(Record.id).label('count')
        ).filter(
            Record.user_id == user_id,
            Record.created_at >= start_datetime,
            Record.created_at <= end_datetime
        ).group_by(func.date(Record.created_at)).all()
        
        count_map = {
            (r.date.isoformat() if hasattr(r.date, 'isoformat') else str(r.date)): r.count 
            for r in daily_counts
        }

        # 3. 组装结果
        history = []
        current_date = start_date
        while current_date <= end_date:
            d_str = current_date.isoformat()
            history.append({
                "date": d_str,
                "atmosphere_color": mood_map.get(d_str, "#CCCCCC"),
                "record_count": count_map.get(d_str, 0)
            })
            current_date += timedelta(days=1)
        
        return history


# 单例
planet_service = PlanetService()
