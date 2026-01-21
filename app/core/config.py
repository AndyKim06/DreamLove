"""
DreamLove 프로젝트 환경 설정 모듈
환경변수 관리 및 설정 클래스 정의
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    .env 파일 또는 환경변수에서 값을 자동으로 로드
    """
    
    # Solar API 설정
    SOLAR_API_KEY: str = ""
    SOLAR_API_URL: str = "https://api.upstage.ai/v1/solar/chat/completions"
    
    # 애플리케이션 설정
    APP_NAME: str = "DreamLove AI Chatbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS 설정
    ALLOW_ORIGINS: list = ["http://127.0.0.1:5500", "http://127.0.0.1:5500", "http://127.0.0.1:8000" ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 전역 설정 인스턴스 생성
settings = Settings()

