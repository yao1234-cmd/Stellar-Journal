"""
Planet API - 星球状态接口
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional

from app.core.database import get_db
from app.schemas.planet import PlanetState, PlanetHistory
from app.services.planet_service import planet_service

router = APIRouter()

# 临时用户ID
TEMP_USER_ID = "00000000-0000-0000-0000-000000000001"


@router.get("/state", response_model=PlanetState)
async def get_planet_state(
    target_date: Optional[str] = Query(None, description="目标日期 YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """
    获取星球当前状态
    
    返回指定日期（默认今天）的星球完整状态：
    - 大气层颜色（当日心情）
    - 灵感星星列表
    - 思考树木列表
    """
    try:
        # 解析日期
        if target_date:
            try:
                parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="日期格式错误，应为 YYYY-MM-DD"
                )
        else:
            parsed_date = date.today()
        
        # 获取星球状态
        state = await planet_service.get_planet_state(
            db=db,
            user_id=TEMP_USER_ID,
            target_date=parsed_date
        )
        
        return state
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取星球状态失败: {str(e)}"
        )


@router.get("/history", response_model=PlanetHistory)
async def get_planet_history(
    days: int = Query(30, ge=1, le=365, description="回溯天数"),
    db: Session = Depends(get_db)
):
    """
    获取星球历史
    
    返回过去N天的星球颜色变化历史，用于时光轴展示
    """
    try:
        history_data = await planet_service.get_planet_history(
            db=db,
            user_id=TEMP_USER_ID,
            days=days
        )
        
        if not history_data:
            return {
                "history": [],
                "start_date": date.today(),
                "end_date": date.today()
            }
        
        return {
            "history": history_data,
            "start_date": history_data[0]["date"],
            "end_date": history_data[-1]["date"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取历史数据失败: {str(e)}"
        )


@router.get("/stats", response_model=dict)
async def get_planet_stats(db: Session = Depends(get_db)):
    """
    获取星球统计信息
    
    返回总体统计数据
    """
    from app.models.record import Record, RecordType
    from sqlalchemy import func
    
    try:
        # 总记录数
        total_records = db.query(func.count(Record.id)).filter(
            Record.user_id == TEMP_USER_ID
        ).scalar() or 0
        
        # 各类型记录数
        mood_count = db.query(func.count(Record.id)).filter(
            Record.user_id == TEMP_USER_ID,
            Record.type == RecordType.MOOD
        ).scalar() or 0
        
        spark_count = db.query(func.count(Record.id)).filter(
            Record.user_id == TEMP_USER_ID,
            Record.type == RecordType.SPARK
        ).scalar() or 0
        
        thought_count = db.query(func.count(Record.id)).filter(
            Record.user_id == TEMP_USER_ID,
            Record.type == RecordType.THOUGHT
        ).scalar() or 0
        
        # 第一条记录日期
        first_record = db.query(Record).filter(
            Record.user_id == TEMP_USER_ID
        ).order_by(Record.created_at).first()
        
        return {
            "total_records": total_records,
            "mood_count": mood_count,
            "spark_count": spark_count,
            "thought_count": thought_count,
            "start_date": first_record.created_at.date().isoformat() if first_record else None,
            "days_active": (date.today() - first_record.created_at.date()).days + 1 if first_record else 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取统计信息失败: {str(e)}"
        )
