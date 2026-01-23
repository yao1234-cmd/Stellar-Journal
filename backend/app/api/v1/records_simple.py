"""
Records API - 简化版（不需要数据库）
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

router = APIRouter()


class RecordCreateSimple(BaseModel):
    """创建记录请求 - 简化版"""
    type: str
    content: str


class RecordResponseSimple(BaseModel):
    """记录响应 - 简化版"""
    id: str
    type: str
    content: str
    color: str
    created_at: str
    message: str


@router.options("/")
async def options_records():
    """处理 OPTIONS 预检请求"""
    return {"status": "ok"}


@router.post("/", response_model=RecordResponseSimple, status_code=status.HTTP_201_CREATED)
async def create_record_simple(record_data: RecordCreateSimple):
    """
    创建记录 - 简化版（不需要数据库和AI）
    
    临时用于测试，后续会替换为完整版本
    """
    print(f"🎉 收到记录请求: type={record_data.type}, content={record_data.content}")
    
    # 根据情绪返回不同颜色
    color_map = {
        "mood": "#87CEEB",  # 天蓝色
        "spark": "#FFD700", # 金黄色
        "thought": "#90EE90"  # 浅绿色
    }
    
    response = {
        "id": str(uuid.uuid4()),
        "type": record_data.type,
        "content": record_data.content,
        "color": color_map.get(record_data.type, "#87CEEB"),
        "created_at": datetime.now().isoformat(),
        "message": f"✅ 成功创建{record_data.type}记录！（简化版，不使用AI和数据库）"
    }
    
    print(f"✅ 返回响应: {response}")
    
    return response


@router.get("/")
async def list_records():
    """获取记录列表 - 简化版"""
    return {
        "records": [],
        "total": 0,
        "message": "简化版：暂无历史记录"
    }
