"""
Record schemas for API validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum
import uuid


class RecordType(str, Enum):
    """记录类型"""
    MOOD = "mood"
    SPARK = "spark"
    THOUGHT = "thought"


class RecordCreate(BaseModel):
    """创建记录请求"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "mood",
                "content": "今天项目顺利完成了，晚上散步看到了很美的夕阳。"
            }
        }
    )
    
    type: RecordType = Field(..., description="记录类型：mood/spark/thought")
    content: str = Field(..., min_length=1, max_length=5000, description="记录内容")
    audio_url: Optional[str] = Field(None, description="音频URL（如果是语音输入）")


class EmotionData(BaseModel):
    """情感分析数据"""
    valence: float = Field(..., ge=0, le=1, description="效价（积极程度）")
    arousal: float = Field(..., ge=0, le=1, description="唤起度（激动程度）")
    primary_emotion: str = Field(..., description="主要情绪")
    emotion_scores: Dict[str, float] = Field(..., description="各情绪得分")


class PositionData(BaseModel):
    """3D位置数据"""
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    orbit_radius: Optional[float] = None
    orbit_angle: Optional[float] = None


class RecordResponse(BaseModel):
    """记录响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    type: RecordType
    content: str
    audio_url: Optional[str] = None
    emotion_analysis: Optional[EmotionData] = None
    keywords: Optional[List[str]] = None
    theme_cluster: Optional[str] = None
    color_hex: Optional[str] = None
    position_data: Optional[PositionData] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class RecordListResponse(BaseModel):
    """记录列表响应"""
    records: List[RecordResponse]
    total: int
    page: int
    page_size: int
