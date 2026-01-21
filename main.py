# ============================================
# 이상형 얼굴 생성기 - 메인 실행 파일 (Ver 6.2)
# ============================================

import sys
sys.path.append('config')
sys.path.append('src')

from config.prompt_config import build_prompt
from src.user_input import get_user_input
from src.flux_api import generate_image


def main():
    """
    메인 실행 함수
    """
    print("=" * 80)
    print("이상형 얼굴 생성기 Ver 6.2")
    print("=" * 80)
    
    # 1. 사용자 입력 받기
    user_choices = get_user_input()
    
    # 2. 프롬프트 생성
    final_prompt = build_prompt(
        gender=user_choices["gender"],
        mood=user_choices["mood"],
        face_shape=user_choices["face_shape"],
        eyelid=user_choices["eyelid"],
        hair=user_choices["hair"],
        clothing=user_choices["clothing"],
        makeup=user_choices["makeup"],
        skin_tone_value=user_choices["skin_tone_value"]
    )
    
    word_count = len(final_prompt.split())
    token_count = int(word_count * 1.15)
    
    print(f"\n📝 생성된 프롬프트:")
    print(f"{final_prompt}")
    print(f"\n📊 단어 수: {word_count} | 예상 토큰: {token_count}")
    
    if token_count > 77:
        print(f"⚠️  경고: 77토큰 초과 (+{token_count - 77})")
    else:
        print("✅ 77토큰 안전!")
    
    # 3. 이미지 생성
    result = generate_image(final_prompt)
    
    if result:
        print(f"\n🎉 완료! 이미지를 확인하세요: {result}")
    else:
        print("\n😢 이미지 생성에 실패했습니다.")


if __name__ == "__main__":
    main()