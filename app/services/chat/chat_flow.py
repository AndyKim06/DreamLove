"""
DreamLove 프로젝트 대화 흐름 관리 모듈
챗봇 시뮬레이션의 전체 대화 로직 및 점수 평가
"""

import json
from typing import Optional
from app.schemas.chatSchemas import UserInfo, IdealType, ChatRequest, ChatResponse, ParsedContext, NegativeFeedbackItem
from app.services.chat.solar_client import query_solar, SolarAPIError
from app.services.chat.concern_parser import parse_concern


async def generate_greeting(user_info: UserInfo, ideal_type: IdealType, parsed_context: ParsedContext) -> str:
    """
    첫 만남에서의 인사말 생성
    
    Args:
        user_info: 사용자 정보
        ideal_type: 이상형 정보
        parsed_context: 추출된 컨텍스트 (장소, 관계, 고민요약)
        
    Returns:
        str: 생성된 인사말
    """
    # 성격 타입에 따른 구체적인 설명
    personality_description = ""
    if ideal_type.personality == "다정한":
        personality_description = "밝고 따뜻하며, 상대방을 배려하고 공감을 잘하는 성격. 부드럽고 친근한 말투를 사용하며, 상대방을 편안하게 만들어주는 스타일"
    else:  # 시크한
        personality_description = "차분하고 쿨한 매력이 있으며, 직설적이지만 센스있는 대화를 하는 성격. 과하지 않게 거리를 유지하면서도 은은한 관심을 표현하는 스타일"
    
    system_prompt = f"""
너는 사용자의 이상형 역할을 하는 데이트 상대입니다.
다음 정보를 바탕으로 자연스럽고 매력적인 첫 인사를 해주세요.

**데이트 상대(당신)의 특징:**
- 성격 유형: {ideal_type.personality}
- 성격 설명: {personality_description}

**상황:**
- 데이트 장소: {parsed_context.location}
- 상대방 이름: {user_info.name}
- 상대방 성별: {user_info.gender}
- 관계: {parsed_context.relationship}

**지침:**
- 첫 만남의 긴장감과 설렘이 느껴지는 자연스러운 인사말을 작성하세요
- 데이트 장소의 분위기를 언급하며 대화를 시작하세요
- 너무 오글거리지 않되, 약간 호감이 느껴지는 톤으로 작성하세요
- 가벼운 질문 1개를 포함하여 자연스럽게 대화를 이어갈 수 있게 하세요
- 2~3문장 정도로 작성하세요
- 성적인 표현, 폭력적 표현, 혐오 표현은 절대 사용하지 마세요

**중요한 출력 규칙:**
- 오직 실제로 말하는 대화 내용만 작성하세요
- 괄호 (...)를 사용한 행동 묘사를 절대 포함하지 마세요
- 별표 *...* 를 사용한 톤이나 분위기 설명을 절대 포함하지 마세요
- "예를 들어", "힌트", "참고" 같은 메타적인 설명을 절대 포함하지 마세요
- 오직 상대방에게 직접 말하는 대사만 작성하세요

"""

    user_prompt = f"""
{parsed_context.location}에서 처음 만난 상황입니다.
상대방({user_info.name})에게 첫 인사를 건네주세요.

다시 한 번 강조: 괄호, 별표, 메타 설명 없이 순수한 대화 내용만 작성하세요.
"""

    try:
        greeting = await query_solar(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.8,
            max_tokens=300
        )
        return greeting
    except SolarAPIError as e:
        # API 오류 시 기본 인사말 반환
        return f"안녕하세요! {parsed_context.location}에서 만나뵙게 되어 반가워요. 여기 분위기 좋네요. 자주 오시는 편인가요?"


async def generate_question(
    stage: int,
    user_info: UserInfo,
    ideal_type: IdealType,
    parsed_context: ParsedContext,
    last_user_message: Optional[str] = None
) -> str:
    """
    대화 단계별 질문 생성
    
    Args:
        stage: 현재 대화 단계 (1~4)
        user_info: 사용자 정보
        ideal_type: 이상형 정보
        parsed_context: 추출된 컨텍스트
        last_user_message: 사용자의 마지막 답변
        
    Returns:
        str: 생성된 질문
    """
    # 성격 타입에 따른 구체적인 설명
    personality_description = ""
    if ideal_type.personality == "다정한":
        personality_description = "밝고 따뜻하며, 상대방을 배려하고 공감을 잘하는 성격. 부드럽고 친근한 말투를 사용하며, 상대방을 편안하게 만들어주는 스타일"
    else:  # 시크한
        personality_description = "차분하고 쿨한 매력이 있으며, 직설적이지만 센스있는 대화를 하는 성격. 과하지 않게 거리를 유지하면서도 은은한 관심을 표현하는 스타일"
    
    system_prompt = f"""
너는 연애 시뮬레이션에서 데이트 상대 역할을 하고 있습니다.

**당신의 특징:**
- 성격 유형: {ideal_type.personality}
- 성격 설명: {personality_description}

**상황:**
- 데이트 장소: {parsed_context.location}
- 상대방: {user_info.name} ({user_info.gender})
- 관계: {parsed_context.relationship}
- 현재 대화 단계: {stage}/5

**역할:**
- 사용자의 이전 답변에 대해 자연스럽게 짧게 반응하세요 (1~2문장)
- 그리고 연애 상황에서 상대의 성격, 가치관, 센스를 파악할 수 있는 의미 있는 질문을 1가지 던지세요
- 질문은 자연스럽고 대화의 흐름에 맞아야 합니다
- 너무 무겁거나 사적인 질문은 피하고, 데이트 분위기에 맞는 질문을 하세요

**주의사항:**
- 한 번에 질문을 여러 개 하지 마세요 (핵심 질문 1개만)
- 성적인 표현, 폭력적 표현, 혐오 표현은 절대 사용하지 마세요
- 점수나 평가에 대해 언급하지 마세요
- 3~5문장 정도로 작성하세요

**중요한 출력 규칙 (매우 중요):**
- **오직 상대방에게 직접 말하는 대사("따옴표 안의 내용")만 출력하세요.**
- "시스템:", "평가 지표:", "참고:", "예시:" 와 같은 설명 텍스트를 절대 포함하지 마세요.
- 괄호(지문)나 별표(*행동묘사*)를 절대 포함하지 마세요.
- 오직 순수한 한국어 구어체 대사만 반환하세요.
- AI 모델 자신의 생각이나 추론 과정을 출력하지 마세요.

"""

    context_text = f"\n\n**사용자의 이전 답변:** {last_user_message}" if last_user_message else ""
    
    user_prompt = f"""
지금은 {stage}번째 대화 차례입니다.
{context_text}

사용자의 답변에 짧게 반응하고, 이어서 연애 능력을 평가할 수 있는 자연스러운 질문을 1가지 해주세요.
"""

    try:
        question = await query_solar(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.8,
            max_tokens=400
        )
        return question
    except Exception:
        # API 오류 또는 기타 예외 시 기본 질문 반환
        default_questions = [
            "그렇군요! 그런데 평소에 스트레스 받을 때는 어떻게 푸시는 편이에요?",
            "재밌네요! 주말에는 보통 뭐 하면서 시간 보내세요?",
            "좋은데요! 만약 데이트 상대가 갑자기 약속을 취소하면 어떻게 반응하실 것 같아요?",
            "그렇구나! 연애할 때 가장 중요하게 생각하는 게 뭐예요?",
            "오, 좋아요! 혹시 기억에 남는 연애 에피소드가 있으세요?"
        ]
        return default_questions[min(stage - 1, len(default_questions) - 1)]


async def evaluate_user_answer(
    user_answer: str,
    user_info: UserInfo,
    ideal_type: IdealType,
    parsed_context: ParsedContext
) -> int:
    """
    사용자 답변 평가 및 점수 부여
    
    Args:
        user_answer: 사용자의 답변
        user_info: 사용자 정보
        ideal_type: 이상형 정보
        parsed_context: 추출된 컨텍스트
        
    Returns:
        int: 점수 변화량 (-10, -5, +5, +10 중 하나)
    """
    system_prompt = f"""
너는 연애 전문 코치이자 평가자입니다.
사용자의 답변이 연애 상황에서 얼마나 매력적이고 건강한 커뮤니케이션인지 평가합니다.

**평가 기준:**
- +10점: 매우 성숙하고 매력적인 답변
  * 배려심과 유머가 적절히 조화됨
  * 공감 능력이 뛰어나고 센스있는 답변
  * 자기 솔직함과 상대 존중의 균형이 좋음
  
- +5점: 무난하고 괜찮은 답변
  * 특별히 문제는 없지만 인상적이진 않음
  * 평범하고 안전한 답변
  
- -5점: 아쉬운 답변
  * 다소 자기중심적이거나 배려가 부족함
  * 어색하거나 맥락에 맞지 않는 답변
  * 소극적이거나 무성의한 느낌
  
- -10점: 매우 비호감적인 답변
  * 무례하거나 공격적인 태도
  * 성의없거나 상대를 무시하는 답변
  * 부적절한 성적 표현이나 혐오 발언

**상황 정보:**
- 데이트 장소: {parsed_context.location}
- 상대방과의 관계: {parsed_context.relationship}
- 이상형의 성격 유형: {ideal_type.personality}
- 사용자 연애 고민: {parsed_context.concern_summary}

**출력 형식:**
반드시 다음 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.
{{"score": 10, "reason": "평가 이유를 한 문장으로"}}

점수는 반드시 -10, -5, 5, 10 중 하나여야 합니다.
"""

    user_prompt = f"""
다음 사용자의 답변을 평가해주세요:

"{user_answer}"

JSON 형식으로 점수와 간단한 이유를 반환하세요.
"""

    try:
        response = await query_solar(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=200
        )
        
        # JSON 파싱
        # 응답에서 JSON 부분만 추출 (```json ``` 등이 포함될 수 있음)
        response = response.strip()
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response)
        score = int(result.get("score", 5))
        
        # 유효한 점수 범위로 보정
        valid_scores = [-10, -5, 5, 10]
        if score not in valid_scores:
            # 가장 가까운 유효한 점수로 매핑
            if score >= 8:
                score = 10
            elif score >= 0:
                score = 5
            elif score >= -7:
                score = -5
            else:
                score = -10
        
        return score
        
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        # 파싱 실패 또는 API 오류 시 기본 점수 반환 (중립)
        # 답변 길이나 간단한 휴리스틱으로 점수 추정
        if len(user_answer.strip()) < 5:
            return -5  # 너무 짧은 답변
        else:
            return 5  # 기본값 (무난한 답변)


async def generate_final_feedback(
    total_score: int,
    user_info: UserInfo,
    ideal_type: IdealType,
    parsed_context: ParsedContext,
    negative_feedbacks: list[NegativeFeedbackItem]
) -> str:
    """
    최종 피드백 생성
    
    Args:
        total_score: 최종 점수
        user_info: 사용자 정보
        ideal_type: 이상형 정보
        parsed_context: 추출된 컨텍스트
        negative_feedbacks: 부정적 평가 내역
        
    Returns:
        str: 최종 피드백 메시지
    """
    
    # 1. 최종 점수가 양수(0점 포함)인 경우: 성공 축하 메시지
    if total_score >= 0:
        if total_score >= 30:
            grade = "매우 성공적"
            emoji = "🌟"
            msg = "완벽해요! 상대방의 마음을 완전히 사로잡으셨군요!"
        elif total_score >= 10:
            grade = "성공적"
            emoji = "😊"
            msg = "좋아요! 매력적인 대화로 좋은 관계를 만들어가고 계시네요."
        else:
            grade = "무난함"
            emoji = "🙂"
            msg = "나쁘지 않아요! 조금 더 자신감을 가져도 좋겠어요."
            
        return f"{emoji} **데이트 시뮬레이션 결과: {grade}** (점수: {total_score}점)\n\n{msg}\n축하합니다! 성공적인 데이트였어요. 실제 연애에서도 이 감각을 잃지 마세요! 💕"

    # 2. 최종 점수가 음수인 경우: 개선 피드백 생성
    grade = "개선 필요"
    emoji = "💪"
    
    # 부정적 피드백 내역 포맷팅
    feedback_context = ""
    for item in negative_feedbacks:
        feedback_context += f"- 질문: {item.question}\n  답변: {item.answer}\n  점수: {item.score}점\n\n"
    
    system_prompt = f"""
너는 연애 전문 코치입니다.
사용자의 데이트 시뮬레이션 점수가 낮게 나왔습니다. 
특히 점수가 깎였던 대화 내용을 분석하여 구체적이고 현실적인 개선 피드백을 주어야 합니다.

**사용자 정보:**
- 이름: {user_info.name}
- 성별: {user_info.gender}
- 상대방과의 관계: {parsed_context.relationship}
- 현재 고민: {parsed_context.concern_summary}

**점수가 깎인 대화 내역:**
{feedback_context}

**피드백 작성 지침:**
1. 위로와 격려 (1문장)
   - "너무 실망하지 마세요" 같은 톤으로 시작

2. 문제점 상세 분석 (필수)
   - **반드시** 아래 형식을 지켜서 점수가 깎인 대화를 먼저 인용하고 피드백을 주세요.
   - 형식:
     "Q. (질문 내용)
      A. (사용자 답변) [점수: -5점/-10점]
      👉 (피드백 내용: 이 답변이 왜 아쉬운지, 어떻게 고치면 좋을지 구체적으로 조언)"

3. 실전 종합 팁 (2~3문장)
   - 사용자의 고민({parsed_context.concern_summary})과 연결하여 종합적인 조언

**주의사항:**
- 각 부정적 피드백 항목마다 질문, 답변, 점수를 정확하게 명시하세요.
- 상처주지 않도록 부드럽고 건설적인 톤으로 작성하세요
- 총 길이 제한 없음 (상세하게 작성)
"""

    user_prompt = f"""
{user_info.name}님의 최종 점수는 {total_score}점입니다.
점수가 깎였던 대화들을 분석하여, 다음번에는 더 나은 대화를 할 수 있도록 따뜻하고 구체적인 피드백을 주세요.
"""

    try:
        feedback = await query_solar(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=800
        )
        
        return f"{emoji} **데이트 시뮬레이션 결과: {grade}** (점수: {total_score}점)\n\n{feedback}"
        
    except SolarAPIError:
        return f"{emoji} **데이트 시뮬레이션 결과: {grade}** (점수: {total_score}점)\n\n아쉬운 결과지만 괜찮아요! 상대방의 입장에서 조금 더 생각하고 배려하는 대화를 시도해보세요. 특히 상대방의 질문에 성의 있게 대답하고, 맞장구를 쳐주는 것만으로도 호감도를 높일 수 있답니다. 다시 도전해보세요!"


async def run_chat_flow(request: ChatRequest) -> ChatResponse:
    """
    전체 채팅 흐름 실행
    
    Args:
        request: 채팅 요청 정보
        
    Returns:
        ChatResponse: 챗봇 응답
    """
    
    # Stage 0: 연애고민에서 컨텍스트 추출 + 첫 인사말 생성
    if request.stage == 0:
        # 1) 연애고민 자연어에서 장소/관계 추출 (없으면 랜덤 생성)
        parsed_context = await parse_concern(request.user_info.concern)
        
        # 2) 첫 인사말 생성
        greeting = await generate_greeting(
            user_info=request.user_info,
            ideal_type=request.ideal_type,
            parsed_context=parsed_context
        )
        
        return ChatResponse(
            bot_message=greeting,
            next_stage=1,
            updated_score=request.current_score,
            score_change=None,
            end=False,
            final_feedback=None,
            parsed_context=parsed_context,  # 프론트엔드에서 저장해야 함!
            negative_feedbacks=[]
        )
    
    # Stage 1~5: 사용자 답변 평가 + 다음 질문 또는 최종 피드백
    try:
        if 1 <= request.stage <= 5:
            # parsed_context가 없으면 에러 (프론트엔드에서 전달해야 함)
            if not request.parsed_context:
                raise ValueError("parsed_context가 필요합니다. Stage 0 응답의 parsed_context를 포함해주세요.")
            
            parsed_context = request.parsed_context
            
            # 1) 사용자의 방금 답변 점수 평가
            score_delta = await evaluate_user_answer(
                user_answer=request.user_message,
                user_info=request.user_info,
                ideal_type=request.ideal_type,
                parsed_context=parsed_context
            )
            new_score = request.current_score + score_delta
            
            # 부정적 평가 기록 (-5 or -10)
            negative_feedbacks = request.negative_feedbacks.copy()
            if score_delta < 0:
                negative_feedbacks.append(NegativeFeedbackItem(
                    question=request.current_question,  # 프론트엔드에서 보내준 현재 질문
                    answer=request.user_message,
                    score=score_delta
                ))
            
            # 2) 아직 마지막 질문 전이라면 → 다음 질문 생성
            if request.stage < 5:
                question = await generate_question(
                    stage=request.stage,
                    user_info=request.user_info,
                    ideal_type=request.ideal_type,
                    parsed_context=parsed_context,
                    last_user_message=request.user_message
                )
                return ChatResponse(
                    bot_message=question,
                    next_stage=request.stage + 1,
                    updated_score=new_score,
                    score_change=score_delta,
                    end=False,
                    final_feedback=None,
                    parsed_context=parsed_context,
                    negative_feedbacks=negative_feedbacks
                )
            
            # 3) 5번째 질문까지 끝났다면 → 최종 피드백
            else:
                feedback = await generate_final_feedback(
                    total_score=new_score,
                    user_info=request.user_info,
                    ideal_type=request.ideal_type,
                    parsed_context=parsed_context,
                    negative_feedbacks=negative_feedbacks
                )
                return ChatResponse(
                    bot_message=feedback,
                    next_stage=6,
                    updated_score=new_score,
                    score_change=score_delta,
                    end=True,
                    final_feedback=feedback,
                    parsed_context=parsed_context,
                    negative_feedbacks=negative_feedbacks
                )
        
        # Stage 6 이후: 이미 종료된 상태 → 간단한 안내 메시지
        return ChatResponse(
            bot_message="이 데이트 시뮬레이션은 이미 종료되었어요. 다시 시작하려면 새로운 세션을 열어주세요.",
            next_stage=request.stage,
            updated_score=request.current_score,
            score_change=None,
            end=True,
            final_feedback=None,
            parsed_context=request.parsed_context,
            negative_feedbacks=request.negative_feedbacks
        )

    except Exception as e:
        # 예상치 못한 오류 발생 시 안전하게 응답 반환
        return ChatResponse(
            bot_message=f"앗, 잠시 머리가 어지럽네요.. (시스템 오류: {str(e)}) \n다시 한 번 말씀해주시겠어요?",
            next_stage=request.stage, # 단계 유지
            updated_score=request.current_score,
            score_change=0,
            end=False,
            final_feedback=None,
            parsed_context=request.parsed_context,
            negative_feedbacks=request.negative_feedbacks
        )

