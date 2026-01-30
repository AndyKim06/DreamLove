"""
DreamLove AI Chatbot 데이터 모델
Pydantic 스키마 정의
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class UserInfo(BaseModel):
    """
    사용자 정보 모델 (간소화됨)
    """
    name: str = Field(..., description="사용자 이름 또는 닉네임")
    gender: Literal["남자", "여자"] = Field(..., description="성별: '남자' 또는 '여자'")
    profile_image: Optional[str] = Field(None, description="프로필 이미지 URL 또는 base64 인코딩된 이미지")
    concern: str = Field(..., description="연애고민 (자연어로 입력, 데이트 장소/관계 자동 추출)")


class ParsedContext(BaseModel):
    """
    연애고민에서 추출된 컨텍스트 정보
    """
    location: str = Field(..., description="추출 또는 자동 생성된 데이트 장소")
    relationship: str = Field(..., description="추출 또는 자동 생성된 상대방과의 관계")
    concern_summary: str = Field(..., description="정리된 연애 고민")



class IdealType(BaseModel):
    """
    이상형 정보 모델
    """
    personality: str = Field(..., description="성격 유형: '다정한' 또는 '시크한'")


class NegativeFeedbackItem(BaseModel):
    """
    부정적인 평가를 받은 대화 내역
    """
    question: str = Field(..., description="당시 AI의 질문")
    answer: str = Field(..., description="사용자의 답변")
    score: int = Field(..., description="받은 점수 (-5 or -10)")


class ChatRequest(BaseModel):
    """
    채팅 요청 모델
    """
    user_info: UserInfo = Field(..., description="사용자 정보")
    ideal_type: IdealType = Field(..., description="이상형 정보")
    parsed_context: Optional[ParsedContext] = Field(None, description="추출된 컨텍스트 (stage 0 이후 자동 설정)")
    user_message: str = Field(default="", description="사용자의 메시지")
    current_question: str = Field(default="", description="사용자가 답변하고 있는 현재 질문 (평가 기록용)")
    stage: int = Field(default=0, ge=0, le=6, description="현재 대화 단계 (0~6)")
    current_score: int = Field(default=0, description="현재까지의 누적 점수")
    negative_feedbacks: list[NegativeFeedbackItem] = Field(default=[], description="누적된 부정적 평가 내역")


class ChatResponse(BaseModel):
    """
    채팅 응답 모델
    """
    bot_message: str = Field(..., description="챗봇의 응답 메시지")
    next_stage: int = Field(..., description="다음 대화 단계")
    updated_score: int = Field(..., description="업데이트된 누적 점수")
    score_change: Optional[int] = Field(None, description="이번 턴에서의 점수 변화량")
    end: bool = Field(..., description="대화 종료 여부")
    final_feedback: Optional[str] = Field(None, description="최종 피드백 (대화 종료 시)")
    parsed_context: Optional[ParsedContext] = Field(None, description="추출된 컨텍스트 정보 (프론트엔드에서 저장 필요)")
    negative_feedbacks: list[NegativeFeedbackItem] = Field(default=[], description="갱신된 부정적 평가 내역")

