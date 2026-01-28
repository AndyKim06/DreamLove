import asyncio
import httpx
import json
import sys

# API 설정
API_URL = "http://localhost:8000/chat/simulate"

async def run_interactive_chat():
    print("\n" + "="*50)
    print("💌 DreamLove 데이트 시뮬레이션 (CLI 모드)")
    print("="*50)
    print("직접 사용자 정보를 입력하고 AI와 대화해보세요!\n")

    # 1. 사용자 정보 입력 받기
    try:
        name = input("👤 이름(닉네임)을 입력하세요: ").strip()
        while not name:
            name = input("   이름은 필수입니다: ").strip()
            
        print("\n성별을 선택하세요:")
        print("1. 남자")
        print("2. 여자")
        gender_choice = input("선택 (1/2): ").strip()
        gender = "남자" if gender_choice == "1" else "여자"
        
        print("\n이상형 스타일을 선택하세요:")
        print("1. 다정한")
        print("2. 시크한")
        style_choice = input("선택 (1/2): ").strip()
        personality = "다정한" if style_choice == "1" else "시크한"
        
        print(f"\n📝 [{name}]님의 연애 고민을 자유롭게 적어주세요.")
        print("(예: 소개팅에서 만난 분이랑 카페에 왔는데 어색해요)")
        concern = input(">>> ").strip()
        while not concern:
            concern = input(">>> ").strip()
            
    except KeyboardInterrupt:
        print("\n⛔ 종료합니다.")
        return

    # 초기 데이터 구성
    user_info = {
        "name": name,
        "gender": gender,
        "profile_image": None,
        "concern": concern
    }
    ideal_type = {
        "personality": personality
    }
    
    # 세션 상태 변수
    session = {
        "parsed_context": None,
        "negative_feedbacks": [],
        "current_score": 0,
        "current_question": ""
    }

    print("\n" + "-"*50)
    print("💞 시뮬레이션을 시작합니다...")
    print("-"*50 + "\n")

    async with httpx.AsyncClient(timeout=60.0) as client:
        # ---------------------------------------------------------
        # Stage 0: 첫 만남
        # ---------------------------------------------------------
        payload = {
            "user_info": user_info,
            "ideal_type": ideal_type,
            "stage": 0,
            "current_score": 0,
            "user_message": "",
            "parsed_context": None,
            "negative_feedbacks": []
        }
        
        try:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # 컨텍스트 저장
            session["parsed_context"] = data["parsed_context"]
            session["current_question"] = data["bot_message"]
            
            ctx = session["parsed_context"]
            print(f"💡 [분석 완료] 장소: {ctx['location']} | 관계: {ctx['relationship']}")
            print(f"\n🌹 그(그녀): \"{data['bot_message']}\"\n")
            
        except httpx.ConnectError:
            print("❌ 서버에 연결할 수 없습니다. 서버가 켜져 있는지 확인해주세요.")
            print("   (터미널에서 'python -m uvicorn app.main:app --reload' 실행 필요)")
            return
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return

        # ---------------------------------------------------------
        # Stage 1 ~ 5: 대화 루프
        # ---------------------------------------------------------
        for stage in range(1, 6):
            # 사용자 입력
            try:
                user_msg = input(f"👤 {name}: ").strip()
                while not user_msg:
                    user_msg = input(f"👤 {name}: ").strip()
            except KeyboardInterrupt:
                print("\n⛔ 대화를 종료합니다.")
                return

            payload = {
                "user_info": user_info,
                "ideal_type": ideal_type,
                "stage": stage,
                "current_score": session["current_score"],
                "user_message": user_msg,
                "parsed_context": session["parsed_context"],
                "negative_feedbacks": session["negative_feedbacks"],
                "current_question": session["current_question"]
            }
            
            print("   (AI가 생각 중입니다... 💭)")
            
            try:
                response = await client.post(API_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # 상태 업데이트
                session["current_score"] = data["updated_score"]
                session["negative_feedbacks"] = data["negative_feedbacks"]
                session["current_question"] = data["bot_message"]
                
                change = data["score_change"]
                # 점수 변화 표시 (디버깅용, 원하면 주석 처리 가능)
                # print(f"   [System] 점수 변화: {change:+d} (현재: {session['current_score']})")
                
                if data["end"]:
                    print("\n" + "="*50)
                    print("🏁 시뮬레이션 결과")
                    print("="*50)
                    print(f"\n{data['final_feedback']}\n")
                    break
                else:
                    print(f"\n🌹 그(그녀): \"{data['bot_message']}\"\n")
                    
            except httpx.HTTPStatusError as e:
                print(f"❌ 서버 오류 ({e.response.status_code}): {e.response.text}")
                break
            except Exception as e:
                print(f"❌ 오류 발생: {e}")
                break

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(run_interactive_chat())
    except ImportError:
        print("❌ 필요한 라이브러리가 없습니다.")
        print("'pip install httpx' 명령어를 실행해주세요.")
