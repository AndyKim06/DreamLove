"""
DreamLove 프로젝트 대화 흐름 관리 모듈
챗봇 시뮬레이션의 전체 대화 로직 및 점수 평가
"""

import json
from typing import Optional
from app.schemas.chatSchemas import UserInfo, IdealType, ChatRequest, ChatResponse, ParsedContext, NegativeFeedbackItem
from app.services.chat.solar_client import query_solar, SolarAPIError
from app.services.chat.concern_parser import parse_concern

FORMAL_RELATIONSHIP_KEYWORDS = [
    "소개팅",
    "첫 만남",
    "첫만남",
    "처음 만남",
    "처음 만난",
]

def is_formal_relationship(relationship: str) -> bool:
    if not relationship:
        return False
    return any(keyword in relationship for keyword in FORMAL_RELATIONSHIP_KEYWORDS)

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
    
    speech_style = "존댓말" if is_formal_relationship(parsed_context.relationship) else "반말"

    # 호칭 규칙 설정
    if speech_style == "반말":
        addressing_rule = f"사용자를 부를 때는 '{user_info.name}아/야' 또는 '너'라고 해. 절대 '{user_info.name}님'이라고 부르지 마."
    else:
        addressing_rule = f"사용자를 부를 때는 '{user_info.name}님'이라고 불러."

    system_prompt = f"""
너는 사용자의 이상형 역할을 하는 데이트 상대야.
{parsed_context.location}에서 약속하고 만난 데이트 상황이야.

**당신의 특징:**
- 성격: {ideal_type.personality}
- 성격 설명: {personality_description}

**상황:**
- 장소: {parsed_context.location}
- 상대방: {user_info.name} ({user_info.gender})
- 관계: {parsed_context.relationship}
- 말투: {speech_style}
- 호칭: {addressing_rule}

**인사말 작성 규칙:**
1. 데이트 약속을 하고 만난 상황이므로 자연스럽고 따뜻하게 인사해
2. **중요: 방금 만난 상황이므로 장소에 대해 '어땠어?' 같은 과거형 질문을 절대 하지 마.** 대신 현재나 직전 상황을 물어봐.
3. 평범하고 현실적인 데이트 인사말로 시작해
4. 반드시 질문은 딱 1개만 해 (절대 2개 이상 금지)
5. 40자 이내로 짧고 간결하게 작성해

**절대 금지:**
- 2개 이상의 질문 (예: "~했어? ~했어?" 형태 금지)
- **장소에 대한 과거형 질문 (예: "카페 어땠어?" -> X)**
- 장소의 냄새, 소리 등 구체적인 감각 묘사
- 괄호, 별표, 화살표 등 메타 설명
- 오글거리거나 과한 표현

**출력:**
오직 상대방에게 직접 말하는 한 문장만 작성해.
"""

    user_prompt = f"""
{parsed_context.location}에서 {user_info.name}님과 데이트 약속을 하고 만났습니다.
자연스럽고 간결한 첫 인사를 해주세요. (질문은 1개만!)
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
        if speech_style == "존댓말":
            return f"안녕하세요! {parsed_context.location}에서 만나뵙게 되어 반가워요. 여기 분위기 좋네요. 자주 오시는 편인가요?"
        return f"안녕! {parsed_context.location}에서 만나서 반가워. 여기 분위기 좋다. 자주 오는 편이야?"


async def generate_question(
    stage: int,
    user_info: UserInfo,
    ideal_type: IdealType,
    parsed_context: ParsedContext,
    conversation_history: list[dict] = None,
    last_user_message: Optional[str] = None
) -> str:
    """
    대화 단계별 질문 생성
    
    Args:
        stage: 현재 대화 단계 (1~4)
        user_info: 사용자 정보
        ideal_type: 이상형 정보
        parsed_context: 추출된 컨텍스트
        conversation_history: 전체 대화 히스토리
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
    
    speech_style = "존댓말" if is_formal_relationship(parsed_context.relationship) else "반말"
    
    # 호칭 규칙 설정
    if speech_style == "반말":
        addressing_rule = f"사용자를 부를 때는 '{user_info.name}아/야' 또는 '너'라고 해. 절대 '{user_info.name}님'이라고 부르지 마."
    else:
        addressing_rule = f"사용자를 부를 때는 '{user_info.name}님'이라고 불러."
    
    # 대화 히스토리가 있으면 활용
    if conversation_history and len(conversation_history) > 0:
        # query_solar_with_history 사용
        from app.services.chat.solar_client import query_solar_with_history
        
        # 이전 대화와 현재 답변을 분리해서 고려
        
        system_prompt_with_history = f"""
너는 사용자의 이상형 역할을 하는 데이트 상대야.

**당신의 특징:**
- 성격: {ideal_type.personality} ({personality_description})
- 장소: {parsed_context.location}
- 관계: {parsed_context.relationship}
- 말투: {speech_style}
- 호칭: {addressing_rule}

**중요 규칙 (반드시 지킬 것):**
1. **사용자의 마지막 말에 먼저 반응해.** (공감, 칭찬, 놀람 등)
   - 예: "정말?", "와 감동이야", "그랬구나" 등으로 시작
2. **절대 인사말을 반복하지 마.** 이미 인사는 끝났어.
3. **질문은 무조건 1개만 해.** (질문 2개 이상 금지)
4. **선택형(A vs B) 질문 절대 금지.** 상대방의 주관적인 생각이나 취향을 묻는 '열린 질문'을 해.
   - 나쁜 예: "영화 볼래 게임 할래?", "짬뽕 좋아해 짜장 좋아해?"
   - 좋은 예: "원래 쉴 땐 주로 어떤 거 해?", "가장 기억에 남는 여행지는 어디야?"
5. **전체 길이는 공백 포함 70자 이내로 짧게!** (필수)
6. 괄호, 별표, 화살표, 글자 수 표시 절대 금지
7. **사용자의 마지막 말:** "{last_user_message}" -> 이 말에 꼭 대답해!
8. **인칭 대명사 변환:** 사용자가 '너'(챗봇)라고 한 건 '나'로, '나'(사용자)라고 한 건 '너'로 바꿔서 이해하고 말해.
   - 예: "너 볼 생각에 좋았어" -> "나 볼 생각에 좋았다니" (O) / "너 볼 생각에 좋았다니" (X)
9. **반응 정확도:** 사용자의 감정(설렘, 기대, 힘듦 등)을 정확히 파악해서 그에 맞는 반응을 해. 엉뚱한 반응 금지.
10. **자연스러운 한국어:** 번역투나 어색한 문장 절대 금지.
11. **출력 형식:** 오직 챗봇의 **'대사'**만 출력해.
    - 금지: "생각하는 과정", "분석 내용", "- 사용자의 감정 반영" 같은 설명 절대 포함하지 마.
12. **주제 유지(중요):** 대화 주제를 갑자기 바꾸지 마. 사용자가 하던 이야기(감정, 상황, 특별한 의미)에 집중해서 그 내용을 더 깊이 물어보거나 공감해. 
    - 뜬금없이 음악, 날씨, 취미 등을 묻는 것 절대 금지.

이전 대화 흐름을 보고, 사용자의 마지막 말에 자연스럽게 반응하면서 대화를 이어가.
"""
        
        try:
            # 히스토리에 마지막 사용자 메시지가 중복 추가되지 않도록 관리 필요하지만
            # 호출부에서 이미 추가해서 넘겨주고 있음 (updated_history)
            # system prompt에 last_user_message를 강조했으므로 LLM이 인식 잘 할 것임
            
            question = await query_solar_with_history(
                system_prompt=system_prompt_with_history,
                conversation_history=conversation_history,
                temperature=0.8,
                max_tokens=400
            )
            if not question or not question.strip():
                raise ValueError("Empty response from Solar API")
            return question
        except Exception:
            # 실패 시 기본 방식으로 폴백
            pass

    # 히스토리가 없거나 실패 시 기본 방식
    system_prompt = f"""
너는 사용자의 이상형 역할을 하는 데이트 상대야.

**당신의 특징:**
- 성격: {ideal_type.personality}
- 성격 설명: {personality_description}

**상황:**
- 장소: {parsed_context.location}
- 상대방: {user_info.name} ({user_info.gender})
- 관계: {parsed_context.relationship}
- 대화 단계: {stage}/5
- 말투: {speech_style}
- 호칭: {addressing_rule}

**대화 목표:**
사용자의 답변 내용과 자연스럽게 이어지는 대화를 해야 해.
사용자가 말한 내용에 공감하거나 반응하면서, 그 주제를 깊이있게 이어가는 질문을 해.

**대화 작성 방법:**
1. 사용자가 방금 한 말의 핵심을 파악해
2. 그 내용에 대해 짧게 공감하거나 반응해 (예: "오", "그렇구나", "좋네" 등)
3. **인칭 대명사 시점 변환:** 사용자의 '너'는 '나'로, '나'는 '너'로 바꿔서 반응해.
4. 사용자가 말한 내용과 관련된 질문을 자연스럽게 이어서 해
5. 전체를 한 문장으로 매끄럽게 연결해


**나쁜 예시 (이렇게 하지 마):**
- 사용자 답변과 동떨어진 질문
- 갑자기 다른 주제로 전환
- 사용자가 언급하지 않은 것을 물어봄
- **A vs B 중 선택하게 하는 질문 (예: "영화가 좋아 드라마가 좋아?")**
- **어색한 한국어 표현 (예: "오늘 뭐하고 지냈어?" -> "오늘 뭐 했어?"로 수정)**
- **갑작스러운 화제 전환 (예: 분위기 좋은데 갑자기 "노래 뭐 좋아해?" 묻기 금지)**

**제약사항:**
- **전체 길이는 70자 이내로 짧게 작성 (필수)**
- **질문은 1개만 (선택형 금지, 서술형 질문 권장)**
- 괄호, 별표, 화살표, 글자 수 표시 절대 금지
- 문법적으로 올바르고 자연스러운 한국어 사용

**출력:**
사용자 답변과 자연스럽게 이어지는 한 문장을 작성해. 글자 수는 절대 표시하지 마.
"""

    context_text = f"\n\n**사용자의 답변:** {last_user_message}" if last_user_message else ""
    
    user_prompt = f"""
대화 {stage}번째 차례입니다.
{context_text}

위 답변의 내용을 잘 파악하고, 그 주제와 자연스럽게 이어지는 반응과 질문을 해주세요.
사용자가 말한 것과 관련된 질문을 해야 합니다!
"""

    try:
        question = await query_solar(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.8,
            max_tokens=400
        )
        if not question or not question.strip():
            raise ValueError("Empty response from Solar API")
        return question
    except Exception:
        # API 오류 또는 기타 예외 시 기본 질문 반환
        if speech_style == "존댓말":
            default_questions = [
                "재밌네요! 주말에는 보통 뭐 하면서 시간 보내세요?",
                "좋은데요! 만약 데이트 상대가 갑자기 약속을 취소하면 어떻게 반응하실 것 같아요?",
                "그렇구나! 연애할 때 가장 중요하게 생각하는 게 뭐예요?",
                "오, 좋아요! 앞으로 저랑은 어떻게 지내고 싶으세요?"
            ]
        else:
            default_questions = [
                "재밌네! 주말에는 보통 뭐 하면서 시간 보내?",
                "좋다! 만약 데이트 상대가 갑자기 약속을 취소하면 어떻게 반응할 것 같아?",
                "그렇구나! 연애할 때 가장 중요하게 생각하는 게 뭐야?",
                "오, 좋아! 앞으로 나랑은 어떻게 지내고 싶어?"
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
            max_tokens=1000  # Pro3 reasoning 모델은 추론에 더 많은 토큰 필요
        )
        if not response or not response.strip():
            raise ValueError("Empty response from Solar API")
        
        # JSON 파싱
        # 응답에서 JSON 부분만 추출 (```json ``` 등이 포함될 수 있음)
        response = response.strip()
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        else:
            # JSON 본문만 있는 경우를 대비해 중괄호 범위 추출
            json_start = response.find("{")
            json_end = response.rfind("}")
            if json_start != -1 and json_end != -1 and json_end > json_start:
                response = response[json_start:json_end + 1].strip()
        
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
    
    # 1. 최종 점수가 양수(0점 초과)인 경우: 성공 축하 메시지
    if total_score > 0:
        if total_score >= 30:
            grade = "매우 성공적"
            msg = "완벽해요! 상대방의 마음을 완전히 사로잡으셨군요!"
        elif total_score >= 10:
            grade = "성공적"
            msg = "좋아요! 매력적인 대화로 좋은 관계를 만들어가고 계시네요."
        else:
            grade = "무난함"
            msg = "나쁘지 않아요! 조금 더 자신감을 가져도 좋겠어요."
            
        return f"**데이트 시뮬레이션 결과: {grade}** (점수: {total_score}점)\n\n{msg}\n축하합니다! 성공적인 데이트였어요. 실제 연애에서도 이 감각을 잃지 마세요!"

    # 2. 최종 점수가 음수인 경우: 개선 피드백 생성
    grade = "개선 필요"
    
    # 부정적 피드백 내역 포맷팅
    feedback_context = ""
    for item in negative_feedbacks:
        feedback_context += f"- 질문: {item.question}\n  답변: {item.answer}\n  점수: {item.score}점\n\n"
    
    system_prompt = f"""
너는 연애 전문 코치입니다.
사용자의 데이트 시뮬레이션 점수가 낮게 나왔습니다. 
특히 점수가 깎였던 대화 내용을 분석하여 구체적이고 현실적인 개선 피드백을 주어야 합니다.

**중요: 이모티콘을 절대 사용하지 마세요!**

**사용자 정보:**
- 이름: {user_info.name}
- 성별: {user_info.gender}
- 상대방과의 관계: {parsed_context.relationship}
- 현재 고민: {parsed_context.concern_summary}

**점수가 깎인 대화 내역:**
{feedback_context}

**[필수] 아래 형식을 반드시 정확히 따르세요:**

{user_info.name}님, (위로와 격려 문장). (전반적인 문제점 2~3문장으로 요약)

---

### **대화별 상세 피드백**

Q. (질문 내용)
A. (사용자 답변) [-점수]
-> (구체적인 조언)

(각 대화마다 위 형식 반복)

### **실전 종합 팁**

(핵심 조언 1~2문장. 예시 없이 간결하게)

**주의사항:**
- 이모티콘 절대 금지
- 반드시 "---" 구분자를 넣어서 요약과 상세를 구분하세요
- "---" 위에는 간단한 요약만, "---" 아래에는 상세 피드백만 작성하세요
- 부드럽고 건설적인 톤으로 작성하세요
- 실전 종합 팁은 예시("예를 들어", "~라고 질문할 수 있습니다" 등) 없이 핵심만 간결하게 작성하세요
"""

    user_prompt = f"""
{user_info.name}님의 최종 점수는 {total_score}점입니다.
점수가 깎였던 대화들을 분석하여, 다음번에는 더 나은 대화를 할 수 있도록 따뜻하고 구체적인 피드백을 주세요.
이모티콘 없이 작성해주세요.
"""

    try:
        feedback = await query_solar(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=1000
        )
        
        return f"**데이트 시뮬레이션 결과: {grade}** (점수: {total_score}점)\n\n{feedback}"
        
    except SolarAPIError:
        return f"**데이트 시뮬레이션 결과: {grade}** (점수: {total_score}점)\n\n아쉬운 결과지만 괜찮아요! 상대방의 입장에서 조금 더 생각하고 배려하는 대화를 시도해보세요. 특히 상대방의 질문에 성의 있게 대답하고, 맞장구를 쳐주는 것만으로도 호감도를 높일 수 있답니다. 다시 도전해보세요!"

async def run_chat_flow(userId, request: ChatRequest) -> ChatResponse:
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
        
        # 아래 코드 실행하면 이상형의 표정변환 사진 3가지 얻을수 있음
        # 프론트엔드에 맞춰서 이미지 경로 보내주고 프론트엔드에서 가져온 경로로 이미지 띄우게 만들어야함
        # ex) idealImagePath = ["~.location_Netural.png", "~.location_Disappointed.png", "~.location_Smiling.png"]
        from app.dependency import getUserService
        parsed_context = await parse_concern(request.user_info.concern)
        idealImagePath = getUserService().getUserIdealImagePath(userId)

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
            ideal_image_base_path=idealImagePath,
            negative_feedbacks=[],
            conversation_history=[{"role": "assistant", "content": greeting}]  # 첫 인사 기록
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
                # 대화 히스토리 업데이트
                updated_history = request.conversation_history.copy()
                updated_history.append({"role": "user", "content": request.user_message})
                
                question = await generate_question(
                    stage=request.stage,
                    user_info=request.user_info,
                    ideal_type=request.ideal_type,
                    parsed_context=parsed_context,
                    conversation_history=updated_history,
                    last_user_message=request.user_message
                )
                
                # 질문을 히스토리에 추가
                updated_history.append({"role": "assistant", "content": question})
                
                return ChatResponse(
                    bot_message=question,
                    next_stage=request.stage + 1,
                    updated_score=new_score,
                    score_change=score_delta,
                    end=False,
                    final_feedback=None,
                    parsed_context=parsed_context,
                    negative_feedbacks=negative_feedbacks,
                    conversation_history=updated_history
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
                    bot_message=f"{request.user_info.name}, 오늘 대화 정말 즐거웠어! 다음에 또 보자! 😊",  # 채팅창에는 작별 인사만
                    next_stage=6,
                    updated_score=new_score,
                    score_change=score_delta,
                    end=True,
                    final_feedback=feedback,  # 결과 페이지용 피드백 데이터는 그대로 전달
                    parsed_context=parsed_context,
                    negative_feedbacks=negative_feedbacks,
                    conversation_history=request.conversation_history
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
            negative_feedbacks=request.negative_feedbacks,
            conversation_history=request.conversation_history
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
            negative_feedbacks=request.negative_feedbacks,
            conversation_history=request.conversation_history
        )

