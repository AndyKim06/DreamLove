"""
DreamLove 프로젝트 Solar Pro 3 API 연동 모듈
Upstage Solar Pro 3 API를 통한 LLM 통신 (Chat 전용 모드, reasoning 미사용)
"""

import httpx
import logging
import re
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class SolarAPIError(Exception):
    """Solar API 호출 중 발생하는 예외"""
    pass


def clean_response(text: str) -> str:
    """
    LLM 응답에서 괄호, 별표 등 메타 설명을 제거하고 순수한 대사만 추출
    
    Args:
        text: LLM의 원본 응답
        
    Returns:
        str: 정제된 대사만 포함된 텍스트
    """
    if not text:
        return text
    
    # 1. 글자 수 표시 제거: (48자), (60자) 등
    text = re.sub(r'\s*\(?\d+자\)?', '', text)
    
    # 2. 괄호 안의 내용 제거: (...), （...）
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'（[^）]*）', '', text)
    
    # 3. 별표 안의 내용 제거: *...*
    text = re.sub(r'\*[^*]*\*', '', text)
    
    # 4. 대괄호 안의 내용 제거: [...]
    text = re.sub(r'\[[^\]]*\]', '', text)
    
    # 5. 화살표 이후의 내용 제거: → ...
    text = re.sub(r'→.*', '', text)

    # 6. 하이픈(-)으로 시작하는 설명문 제거 (줄 끝에 붙은 경우)
    # 예: "대사" - 설명...
    if '"' in text or "'" in text:
         # 다옴표가 닫힌 뒤에 나오는 - ... 제거
         text = re.sub(r'(["\'])[\s]*-[^\1]*$', r'\1', text)
    
    # 7. 연속된 공백 정리
    text = re.sub(r'\s+', ' ', text)
    
    # 7. 앞뒤 공백 제거
    text = text.strip()
    
    return text


async def query_solar(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.8,
    max_tokens: int = 1000
) -> str:
    """
    Upstage Solar Pro 3 API에 쿼리를 보내고 응답을 받는 함수 (Chat 전용 모드)
    
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
        "model": "solar-pro3",  # Chat 전용 모드 (reasoning 파라미터 미사용)
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
        "stream": False,
        "reasoning_effort": "low"
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            logger.info(f"Solar API 요청: {settings.SOLAR_API_URL}")
            response = await client.post(
                settings.SOLAR_API_URL,
                headers=headers,
                json=payload
            )
            
            logger.info(f"Solar API 응답 상태: {response.status_code}")
            response.raise_for_status()
            
            response_text = response.text
            logger.debug(f"Solar API 원본 응답: {response_text[:500]}")
            
            if not response_text or not response_text.strip():
                raise SolarAPIError("API가 빈 응답을 반환했습니다.")
            
            result = response.json()
            
            # 전체 응답 구조 로깅 (디버깅용)
            logger.info(f"Solar API 전체 응답: {result}")
            
            # Solar Pro3 API 응답에서 텍스트 추출
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                content = message.get("content")
                
                logger.info(f"content: {content}")
                
                # Chat 모드에서는 content에 응답이 들어옴
                if content and content.strip():
                    # 괄호/별표 등 메타 설명 제거 후 반환
                    cleaned = clean_response(content.strip())
                    logger.info(f"cleaned content: {cleaned}")
                    return cleaned
                else:
                    # content가 비어있으면 에러 (reasoning 폴백 제거 - 영어 추론 방지)
                    raise SolarAPIError(f"응답 content가 비어있습니다. message: {message}")
            else:
                logger.error(f"잘못된 응답 형식: {result}")
                raise SolarAPIError(f"응답 형식이 올바르지 않습니다: {result}")
                
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
        "model": "solar-pro3",  # Chat 전용 모드 (reasoning 파라미터 미사용)
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "reasoning_effort": "low"
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
                # 괄호/별표 등 메타 설명 제거 후 반환
                cleaned = clean_response(result["choices"][0]["message"]["content"].strip())
                return cleaned
            else:
                raise SolarAPIError("응답 형식이 올바르지 않습니다.")
                
    except httpx.HTTPStatusError as e:
        raise SolarAPIError(f"HTTP 오류 발생: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        raise SolarAPIError(f"요청 오류 발생: {str(e)}")
    except Exception as e:
        raise SolarAPIError(f"예상치 못한 오류 발생: {str(e)}")

