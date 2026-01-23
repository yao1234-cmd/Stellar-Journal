"""
Emotion analysis schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict


class EmotionAnalysis(BaseModel):
    """情感分析结果"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "valence": 0.75,
                "arousal": 0.5,
                "primary_emotion": "joy",
                "emotion_scores": {
                    "joy": 0.8,
                    "calm": 0.6,
                    "anxiety": 0.1
                },
                "color_hex": "#87CEEB"
            }
        }
    )
    
    valence: float = Field(..., ge=0, le=1, description="效价：0=消极，1=积极")
    arousal: float = Field(..., ge=0, le=1, description="唤起度：0=平静，1=激动")
    primary_emotion: str = Field(..., description="主要情绪")
    emotion_scores: Dict[str, float] = Field(..., description="各情绪得分")
    color_hex: str = Field(..., description="映射的颜色")