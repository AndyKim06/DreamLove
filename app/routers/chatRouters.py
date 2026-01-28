"""
DreamLove 프로젝트 채팅 API 라우터
채팅 시뮬레이션 관련 엔드포인트
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.chatSchemas import ChatRequest, ChatResponse
from app.services.chat.chat_flow import run_chat_flow
from app.services.chat.solar_client import SolarAPIError


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post(
    "/simulate",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="연애 시뮬레이션 채팅",
    description="사용자 정보와 이상형 정보를 기반으로 AI 챗봇과 연애 시뮬레이션 대화를 진행합니다."
)
async def simulate_chat(request: ChatRequest) -> ChatResponse:
    """
    연애 시뮬레이션 채팅 엔드포인트
    
    Args:
        request: 채팅 요청 정보 (사용자 정보, 이상형 정보, 메시지, 단계, 점수)
        
    Returns:
        ChatResponse: 챗봇 응답 (메시지, 다음 단계, 점수, 종료 여부)
        
    Raises:
        HTTPException: API 호출 실패 또는 처리 오류 시
    """
    try:
        # 대화 흐름 실행
        response = await run_chat_flow(request)
        return response
        
    except SolarAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 오류: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"잘못된 요청: {str(e)}"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()  # 서버 콘솔에 상세 에러 출력
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 오류: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="채팅 서비스 헬스체크",
    description="채팅 서비스의 상태를 확인합니다."
)
async def health_check():
    """
    채팅 서비스 헬스체크 엔드포인트
    """
    return {
        "status": "healthy",
        "service": "chat",
        "message": "채팅 서비스가 정상 작동 중입니다."
    }

