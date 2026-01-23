"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="星迹 - 将情感转化为宇宙的记录应用",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # 从配置读取
    allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,  # Vercel 通配符支持
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "message": "让每一次内心波动，都成为构建独特宇宙的星辰 ✨"
    }


@app.options("/{full_path:path}")
async def options_handler():
    """处理所有 OPTIONS 预检请求"""
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }


@app.post("/api/v1/test")
async def test_endpoint(data: dict):
    """测试端点 - 不需要数据库"""
    print(f"收到POST请求: {data}")  # 在终端打印
    return {"success": True, "received": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

