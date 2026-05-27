import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from utils.exception_handlers import register_exception_handlers
from utils.logger import get_logger
from utils.rate_limiter import limiter


logger = get_logger("main")
app = FastAPI(
    title="新闻资讯平台API",
    description="基于FastAPI构建的高性能新闻资讯平台后端系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# 注册限流器
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda req, exc: {
    "code": 429,
    "message": "请求过于频繁，请稍后再试",
    "data": None
})

register_exception_handlers(app)

# CORS 配置（从环境变量读取允许的来源）
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    logger.info("访问根路径")
    return {"message": "Hello World", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "code": 200}

#注册路由
app.include_router(news.router)

app.include_router(users.router)

app.include_router(favorite.router)

app.include_router(history.router)

logger.info("应用启动完成")