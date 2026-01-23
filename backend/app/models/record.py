"""
Record model - 记录模型（心情、灵感、思考）
"""
from sqlalchemy import Column, String, DateTime, Float, Text, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from app.core.database import Base


class RecordType(enum.Enum):
    """记录类型枚举"""
    MOOD = "mood"        # 心情
    SPARK = "spark"      # 灵感
    THOUGHT = "thought"  # 思考


class Record(Base):
    """记录表"""
    __tablename__ = "records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 记录基本信息
    type = Column(SQLEnum(RecordType), nullable=False, index=True)
    content = Column(Text, nullable=False)
    audio_url = Column(String(512), nullable=True)  # 语音记录的URL（如果有）
    
    # AI 分析结果
    emotion_analysis = Column(JSON, nullable=True)  # 情感分析结果
    """
    示例结构：
    {
        "valence": 0.8,      # 效价 (0-1, 消极到积极)
        "arousal": 0.6,      # 唤起度 (0-1, 平静到激动)
        "primary_emotion": "joy",
        "emotion_scores": {
            "joy": 0.8,
            "calm": 0.6,
            "anxiety": 0.1
        }
    }
    """
    
    keywords = Column(JSON, nullable=True)  # 提取的关键词（用于灵感和思考）
    """
    示例: ["工作", "创意", "设计"]
    """
    
    theme_cluster = Column(String(100), nullable=True)  # 主题聚类ID（用于思考树）
    
    # 可视化相关
    color_hex = Column(String(7), nullable=True)  # 星球颜色 #RRGGBB
    position_data = Column(JSON, nullable=True)  # 3D空间位置数据
    """
    示例：
    {
        "x": 0.5,
        "y": 1.2,
        "z": -0.8,
        "orbit_radius": 2.0,  # 星星轨道半径
        "orbit_angle": 45     # 星星轨道角度
    }
    """
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Record {self.type.value} at {self.created_at}>"
