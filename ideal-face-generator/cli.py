# cli.py - CLI 기반 이상형 이미지 생성

from prompts import PromptBuilder
from generator import generate_image

def main():
    print("=" * 60)
    print("이상형 이미지 생성기 (FLUX.1-dev)")
    print("=" * 60)
    
    # 성별 선택
    print("\n[성별 선택]")
    print("1. 여자")
    print("2. 남자")
    gender_choice = input("선택 (1-2): ").strip()
    gender = "female" if gender_choice == "1" else "male"
    
    # 동물상 선택
    print(f"\n[동물상 선택]")
    if gender == "female":
        print("1. 강아지상")
        print("2. 고양이상")
        print("3. 토끼상")
        print("4. 사슴상")
        animal_map = {"1": "puppy", "2": "cat", "3": "rabbit", "4": "deer"}
    else:
        print("1. 강아지상")
        print("2. 여우상")
        print("3. 공룡상")
        print("4. 곰상")
        animal_map = {"1": "puppy", "2": "fox", "3": "dinosaur", "4": "bear"}
    
    animal_choice = input("선택 (1-4): ").strip()
    animal = animal_map[animal_choice]
    
    # 눈꺼풀
    print("\n[눈꺼풀]")
    print("1. 무쌍")
    print("2. 쌍커풀")
    eyelid_choice = input("선택 (1-2): ").strip()
    eyelid = "monolid" if eyelid_choice == "1" else "double"
    
    # 얼굴형
    print("\n[얼굴형]")
    print("1. 둥근형")
    print("2. V라인")
    face_choice = input("선택 (1-2): ").strip()
    face_shape = "round" if face_choice == "1" else "v-line"
    
    # 헤어스타일
    print("\n[헤어스타일]")
    print("1. 긴머리")
    print("2. 단발")
    print("3. 숏컷")
    hairstyle_map = {"1": "long", "2": "short-bob", "3": "short"}
    hairstyle_choice = input("선택 (1-3): ").strip()
    hairstyle = hairstyle_map[hairstyle_choice]
    
    # 옷
    print("\n[옷]")
    print("1. 셔츠")
    print("2. 니트")
    print("3. 후드")
    clothing_map = {"1": "shirt", "2": "knit", "3": "hoodie"}
    clothing_choice = input("선택 (1-3): ").strip()
    clothing = clothing_map[clothing_choice]
    
    # 메이크업
    print("\n[메이크업/스타일링]")
    print("1. 연하게")
    print("2. 진하게")
    makeup_choice = input("선택 (1-2): ").strip()
    makeup = "light" if makeup_choice == "1" else "heavy"
    
    # 피부톤
    print("\n[피부톤]")
    print("0-100 사이 값 (0-25: 13호, 26-50: 21호, 51-75: 23호, 76-100: 28호)")
    skintone = int(input("입력: ").strip())
    
    # 생성 개수
    print("\n[생성 개수]")
    print("몇 장 생성할까요? (1-10, 권장: 4)")
    num_choice = input("입력 (기본 4): ").strip()
    num_images = int(num_choice) if num_choice else 4
    num_images = max(1, min(10, num_images))  # 1-10 범위 제한
    
    # 프롬프트 생성
    print("\n" + "=" * 60)
    print("프롬프트 생성 중...")
    print("=" * 60)
    
    prompt_eng, negative_prompt, prompt_kor, tokens = PromptBuilder.build_prompt(
        gender, animal, eyelid, face_shape, 
        hairstyle, clothing, makeup, skintone
    )
    
    print(f"\n최종 프롬프트: {prompt_kor}")
    print(f"토큰 수: {tokens}/512 (FLUX 최대)")
    print(f"\n영문 프롬프트:")
    print("-" * 60)
    print(prompt_eng)
    print("-" * 60)
    
    # 이미지 생성
    print("\n" + "=" * 60)
    result_files = generate_image(prompt_eng, negative_prompt, prompt_kor, num_images=num_images)
    print("=" * 60)
    
    if result_files:
        print(f"\n{len(result_files)}장 생성됨")
        print("\noutput 폴더에서 마음에 드는 이미지를 선택하세요!")
    else:
        print("\n생성 실패")

if __name__ == "__main__":
    main()