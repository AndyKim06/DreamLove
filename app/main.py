"""
DreamLove AI Chatbot Backend
FastAPI 메인 애플리케이션
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import chatRouters

# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="연애 시뮬레이션 AI 챗봇 DreamLove의 백엔드 API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(chatRouters.router)


@app.get("/")
async def root():
    """
    루트 엔드포인트
    API 기본 정보 반환
    """
    return {
        "message": "Welcome to DreamLove AI Chatbot API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/chat/health"
    }


@app.get("/health")
async def health():
    """
    전체 서비스 헬스체크
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

