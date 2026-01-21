"""
Planet schemas - 星球状态相关
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from datetime import date as DateType


class StarElement(BaseModel):
    """星星元素"""
    id: str
    position: Dict[str, float]  # {x, y, z, orbit_radius, orbit_angle}
    color: str
    size: float
    keyword: str


class TreeElement(BaseModel):
    """树木元素"""
    id: str
    position: Dict[str, float]  # {x, y, z}
    theme: str
    leaf_count: int
    size: float


class PlanetState(BaseModel):
    """星球当前状态"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2024-05-15",
                "atmosphere_color": "#8B7EC8",
                "stars": [
                    {
                        "id": "star-1",
                        "position": {"x": 0, "y": 0, "z": 2, "orbit_radius": 2, "orbit_angle": 45},
                        "color": "#FFD700",
                        "size": 0.1,
                        "keyword": "创意"
                    }
                ],
                "trees": [],
                "total_records": 5
            }
        }
    )
    
    date: DateType = Field(..., description="日期")
    atmosphere_color: str = Field(..., description="大气层颜色（当日心情）")
    stars: List[StarElement] = Field(default_factory=list, description="灵感星星列表")
    trees: List[TreeElement] = Field(default_factory=list, description="思考树木列表")
    total_records: int = Field(..., description="总记录数")


class PlanetHistoryItem(BaseModel):
    """历史某一天的星球快照"""
    date: DateType
    atmosphere_color: str
    record_count: int


class PlanetHistory(BaseModel):
    """星球历史"""
    history: List[PlanetHistoryItem]
    start_date: DateType
    end_date: DateType
