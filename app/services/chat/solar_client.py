"""
DreamLove 프로젝트 Solar Pro 2 API 연동 모듈
Upstage Solar Pro 2 API를 통한 LLM 통신
"""

import httpx
from typing import Optional, Dict, Any
from app.core.config import settings


class SolarAPIError(Exception):
    """Solar API 호출 중 발생하는 예외"""
    pass


async def query_solar(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    Upstage Solar Pro 2 API에 쿼리를 보내고 응답을 받는 함수
    
    Args:
        system_prompt: 시스템 프롬프트 (챗봇의 역할 및 설정)
        user_prompt: 사용자 프롬프트 (실제 질문 또는 대화 내용)
        temperature: 응답의 창의성 조절 (0.0 ~ 1.0)
        max_tokens: 최대 생성 토큰 수
        
    Returns:
        str: AI의 응답 텍스트
        
    Raises:
        SolarAPIError: API 호출 실패 시
    """
    
    headers = {
        "Authorization": f"Bearer {settings.SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "solar-pro3",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "reasoning_effort": "high", 
        "stream": True,
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.SOLAR_API_URL,
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Solar API 응답에서 텍스트 추출
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                raise SolarAPIError("응답 형식이 올바르지 않습니다.")
                
    except httpx.HTTPStatusError as e:
        raise SolarAPIError(f"HTTP 오류 발생: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        raise SolarAPIError(f"요청 오류 발생: {str(e)}")
    except Exception as e:
        raise SolarAPIError(f"예상치 못한 오류 발생: {str(e)}")


async def query_solar_with_history(
    system_prompt: str,
    conversation_history: list[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    대화 히스토리를 포함한 Solar API 쿼리
    
    Args:
        system_prompt: 시스템 프롬프트
        conversation_history: 대화 히스토리 리스트 [{"role": "user/assistant", "content": "..."}]
        temperature: 응답의 창의성 조절
        max_tokens: 최대 생성 토큰 수
        
    Returns:
        str: AI의 응답 텍스트
    """
    
    headers = {
        "Authorization": f"Bearer {settings.SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    
    payload = {
        "model": "solar-pro3",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.SOLAR_API_URL,
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                raise SolarAPIError("응답 형식이 올바르지 않습니다.")
                
    except httpx.HTTPStatusError as e:
        raise SolarAPIError(f"HTTP 오류 발생: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        raise SolarAPIError(f"요청 오류 발생: {str(e)}")
    except Exception as e:
        raise SolarAPIError(f"예상치 못한 오류 발생: {str(e)}")

