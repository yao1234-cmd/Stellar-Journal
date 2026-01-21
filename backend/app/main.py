"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

# #region agent log
import json
from datetime import datetime
def log_debug(location, message, data):
    try:
        with open(r'd:\Planet\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"location": location, "message": message, "data": data, "timestamp": datetime.now().timestamp() * 1000, "sessionId": "debug-session"}, ensure_ascii=False) + '\n')
    except: pass
# #endregion

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="星迹 - 将情感转化为宇宙的记录应用",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# #region agent log
log_debug("main.py:30", "FastAPI app initialized", {"app_name": settings.APP_NAME, "api_prefix": settings.API_V1_PREFIX, "hypothesisId": "A"})
# #endregion

# CORS middleware - 使用更宽松的配置用于调试
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源（调试用）
    allow_credentials=False,  # 关闭凭证以配合 allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# #region agent log
log_debug("main.py:41", "CORS middleware configured", {"allow_origins": "*", "hypothesisId": "C"})
# #endregion

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# #region agent log
log_debug("main.py:36", "API router included", {"prefix": settings.API_V1_PREFIX, "routes_count": len(api_router.routes), "route_paths": [r.path for r in api_router.routes], "hypothesisId": "A"})
# #endregion


@app.get("/")
async def root():
    """Health check endpoint"""
    # #region agent log
    log_debug("main.py:42", "Root endpoint called", {"all_routes": [{"path": r.path, "methods": r.methods} for r in app.routes], "hypothesisId": "A"})
    # #endregion
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

