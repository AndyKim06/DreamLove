"""
DreamLove 프로젝트 연애고민 파서 모듈
자연어로 입력된 연애고민에서 데이트 장소, 관계를 추출하고
명시되지 않은 경우 자동 생성
"""

import json
import random
from typing import Optional
from app.schemas.chatSchemas import ParsedContext
from app.services.chat.solar_client import query_solar, SolarAPIError


# 랜덤 선택용 기본값
DEFAULT_LOCATIONS = [
    "카페", "레스토랑", "영화관", "한강", 
    "놀이공원", "미술관", "맛집", "와인바"
]

DEFAULT_RELATIONSHIPS = [
    "첫 만남", "소개팅", "썸 타는 사이", "연인", 
    "오래된 연인", "짝사랑"
]


async def parse_concern(concern: str) -> ParsedContext:
    """
    사용자의 연애고민 자연어 입력에서 컨텍스트 추출
    
    Args:
        concern: 사용자가 입력한 연애고민 자연어 텍스트
        
    Returns:
        ParsedContext: 추출된 데이트 장소, 관계, 정리된 고민
    """
    
    system_prompt = """
너는 연애 상담 전문가입니다. 사용자의 연애 고민에서 정보를 추출해야 합니다.

**추출해야 할 정보:**
1. location: 데이트 장소 (언급된 경우)
2. relationship: 상대방과의 관계 (언급된 경우)
3. concern_summary: 핵심 고민 요약 (1~2문장)

**규칙:**
- 명시적으로 언급되지 않은 정보는 null로 표시하세요
- 장소가 구체적으로 언급되면 그대로 사용 (예: "카페", "영화관", "한강")
- 관계가 언급되면 적절히 분류 (예: "첫 만남", "소개팅", "썸", "연인", "짝사랑" 등)
- 고민 요약은 핵심만 간결하게

**출력 형식 (JSON만 출력):**
{"location": "장소 또는 null", "relationship": "관계 또는 null", "concern_summary": "핵심 고민 요약"}
"""

    user_prompt = f"""
다음 연애 고민에서 정보를 추출해주세요:

"{concern}"

JSON 형식으로만 응답하세요.
"""

    try:
        response = await query_solar(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=300
        )
        
        # JSON 파싱
        response = response.strip()
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response)
        
        # null이거나 비어있는 값은 랜덤으로 채움
        location = result.get("location")
        if not location or location == "null" or location.lower() == "null":
            location = random.choice(DEFAULT_LOCATIONS)
            
        relationship = result.get("relationship")
        if not relationship or relationship == "null" or relationship.lower() == "null":
            relationship = random.choice(DEFAULT_RELATIONSHIPS)
            
        concern_summary = result.get("concern_summary", concern)
        if not concern_summary:
            concern_summary = concern
        
        return ParsedContext(
            location=location,
            relationship=relationship,
            concern_summary=concern_summary
        )
        
    except (json.JSONDecodeError, ValueError, KeyError, SolarAPIError) as e:
        # 파싱 실패 시 기본값 + 원본 고민 사용
        return ParsedContext(
            location=random.choice(DEFAULT_LOCATIONS),
            relationship=random.choice(DEFAULT_RELATIONSHIPS),
            concern_summary=concern
        )


def get_random_context(concern: str) -> ParsedContext:
    """
    AI 호출 없이 랜덤 컨텍스트 생성 (백업용)
    
    Args:
        concern: 원본 연애고민
        
    Returns:
        ParsedContext: 랜덤 생성된 컨텍스트
    """
    return ParsedContext(
        location=random.choice(DEFAULT_LOCATIONS),
        relationship=random.choice(DEFAULT_RELATIONSHIPS),
        concern_summary=concern
    )
