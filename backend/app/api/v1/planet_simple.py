"""
Planet API - 简化版（不需要数据库）
"""
from fastapi import APIRouter, Query
from typing import Optional
from datetime import date, datetime, timedelta

router = APIRouter()

# 临时用户ID
TEMP_USER_ID = "00000000-0000-0000-0000-000000000001"


@router.get("/state")
async def get_planet_state(
    target_date: Optional[str] = Query(None, description="目标日期 YYYY-MM-DD"),
):
    """
    获取星球当前状态（模拟数据）
    """
    # #region agent log
    import json
    from datetime import datetime as dt
    try:
        with open(r'd:\Planet\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"location": "planet_simple.py:20", "message": "get_planet_state called", "data": {"target_date": target_date, "hypothesisId": "F"}, "timestamp": dt.now().timestamp() * 1000, "sessionId": "debug-session"}, ensure_ascii=False) + '\n')
    except: pass
    # #endregion
    
    today = date.today()
    target = datetime.strptime(target_date, "%Y-%m-%d").date() if target_date else today
    
    return {
        "date": target.isoformat(),
        "atmosphere_color": "#4a5568",  # 默认灰蓝色
        "stars": [],  # 暂时没有星星
        "trees": [],  # 暂时没有树木
        "total_records": 0
    }


@router.get("/history")
async def get_planet_history(
    days: int = Query(30, ge=1, le=365, description="回溯天数"),
):
    """
    获取星球历史（模拟数据）
    """
    today = date.today()
    history = []
    
    for i in range(days):
        day = today - timedelta(days=i)
        history.append({
            "date": day.isoformat(),
            "atmosphere_color": "#4a5568",
            "record_count": 0
        })
    
    history.reverse()  # 按时间正序排列
    
    return {
        "history": history,
        "start_date": history[0]["date"] if history else today.isoformat(),
        "end_date": history[-1]["date"] if history else today.isoformat()
    }


@router.get("/stats")
async def get_planet_stats():
    """
    获取星球统计信息（模拟数据）
    """
    return {
        "total_records": 0,
        "mood_count": 0,
        "spark_count": 0,
        "thought_count": 0,
        "start_date": None,
        "days_active": 0
    }
