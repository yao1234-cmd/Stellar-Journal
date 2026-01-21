"""
API V1 Router
"""
from fastapi import APIRouter
from app.api.v1 import records, planet  # 使用完整版（带数据库）

api_router = APIRouter()

# Include sub-routers - 使用完整版本（使用数据库）
api_router.include_router(records.router, prefix="/records", tags=["records"])
api_router.include_router(planet.router, prefix="/planet", tags=["planet"])
