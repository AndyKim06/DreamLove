import asyncio
import httpx
import json

# API 설정
API_URL = "http://localhost:8000/chat/simulate"

# 실패한 케이스 데이터
user_info = {
    "name": "rlr",
    "gender": "남자",
    "profile_image": None,
    "concern": "레스토랑에서 소개팅하기로 했는데 무슨말할지 모르겠어"
}
ideal_type = {
    "personality": "다정한"
}
parsed_context = {
    "dating_place": "레스토랑",
    "relationship": "소개팅",
    "concern_summary": "레스토랑에서 소개팅하기로 했는데 무슨말할지 모르겠어"
}

async def run_debug_test():
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Stage 1: "너가 추천해줘" 라고 했을 때 에러 발생
        print(f"🚀 디버그 테스트 시작: {API_URL}")
        
        payload = {
            "user_info": user_info,
            "ideal_type": ideal_type,
            "stage": 1,
            "current_score": 0,
            "user_message": "너가 추천해줘",
            "parsed_context": parsed_context,
            "negative_feedbacks": [],
            "current_question": "혹시 어떤 음식 좋아하세요? 메뉴 추천도 부탁드려도 될까요? 😊"
        }
        
        print("\n[요청 데이터]")
        print(json.dumps(payload, indent=2, ensure_ascii=False))

        try:
            response = await client.post(API_URL, json=payload)
            print(f"\n[응답 상태 코드]: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[응답 내용]: {response.text}")
            else:
                print(f"[성공]: {response.json()}")
                
        except Exception as e:
            print(f"\n❌ 요청 중 예외 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run_debug_test())
