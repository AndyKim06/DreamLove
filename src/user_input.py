# ============================================
# 콘솔 사용자 입력 처리
# ============================================

def get_user_input():
    """
    콘솔에서 사용자 선택 입력 받기
    
    Returns:
        dict: 사용자가 선택한 옵션들
    """
    print("\n" + "="*60)
    print("✨ 이상형 얼굴 생성기 ✨")
    print("="*60)
    
    # 1. 성별 선택
    print("\n[1] 성별을 선택하세요:")
    print("  1. 여성")
    print("  2. 남성")
    while True:
        choice = input("선택 (1-2): ").strip()
        if choice == "1":
            gender = "여성"
            break
        elif choice == "2":
            gender = "남성"
            break
        else:
            print("1 또는 2를 입력하세요.")
    
    # 2. 분위기 선택
    print("\n[2] 분위기를 선택하세요:")
    print("  1. 청순")
    print("  2. 시크")
    print("  3. 귀여운")
    while True:
        choice = input("선택 (1-3): ").strip()
        if choice == "1":
            mood = "청순"
            break
        elif choice == "2":
            mood = "시크"
            break
        elif choice == "3":
            mood = "귀여운"
            break
        else:
            print("1, 2, 3 중 하나를 입력하세요.")
    
    # 3. 얼굴형 선택
    print("\n[3] 얼굴형을 선택하세요:")
    print("  1. 둥근형")
    print("  2. V라인")
    while True:
        choice = input("선택 (1-2): ").strip()
        if choice == "1":
            face_shape = "둥근형"
            break
        elif choice == "2":
            face_shape = "V라인"
            break
        else:
            print("1 또는 2를 입력하세요.")
    
    # 4. 쌍커풀 선택
    print("\n[4] 쌍커풀을 선택하세요:")
    print("  1. 무쌍")
    print("  2. 겉쌍")
    while True:
        choice = input("선택 (1-2): ").strip()
        if choice == "1":
            eyelid = "무쌍"
            break
        elif choice == "2":
            eyelid = "겉쌍"
            break
        else:
            print("1 또는 2를 입력하세요.")
    
    # 5. 헤어스타일 선택
    print("\n[5] 헤어스타일을 선택하세요:")
    print("  1. 긴머리")
    print("  2. 단발")
    print("  3. 숏컷")
    while True:
        choice = input("선택 (1-3): ").strip()
        if choice == "1":
            hair = "긴머리"
            break
        elif choice == "2":
            hair = "단발"
            break
        elif choice == "3":
            hair = "숏컷"
            break
        else:
            print("1, 2, 3 중 하나를 입력하세요.")
    
    # 6. 옷 선택
    print("\n[6] 옷을 선택하세요:")
    print("  1. 셔츠")
    print("  2. 니트")
    print("  3. 후드티")
    while True:
        choice = input("선택 (1-3): ").strip()
        if choice == "1":
            clothing = "셔츠"
            break
        elif choice == "2":
            clothing = "니트"
            break
        elif choice == "3":
            clothing = "후드티"
            break
        else:
            print("1, 2, 3 중 하나를 입력하세요.")
    
    # 7. 메이크업 강도 선택
    print("\n[7] 메이크업 강도를 선택하세요:")
    print("  1. 연하게")
    print("  2. 진하게")
    while True:
        choice = input("선택 (1-2): ").strip()
        if choice == "1":
            makeup = "연하게"
            break
        elif choice == "2":
            makeup = "진하게"
            break
        else:
            print("1 또는 2를 입력하세요.")
    
    # 8. 피부톤 슬라이더 (0.0 ~ 1.0)
    print("\n[8] 피부톤을 입력하세요 (0.0~1.0):")
    print("  0.0 = 매우 밝음 (13호)")
    print("  0.5 = 보통 (21호)")
    print("  1.0 = 어두움 (28호)")
    while True:
        try:
            skin_tone = float(input("피부톤 값: ").strip())
            if 0.0 <= skin_tone <= 1.0:
                break
            else:
                print("0.0 ~ 1.0 사이의 값을 입력하세요.")
        except ValueError:
            print("숫자를 입력하세요.")
    
    print("\n" + "="*60)
    print("모든 선택이 완료되었습니다!")
    print("="*60)
    
    return {
        "gender": gender,
        "mood": mood,
        "face_shape": face_shape,
        "eyelid": eyelid,
        "hair": hair,
        "clothing": clothing,
        "makeup": makeup,
        "skin_tone_value": skin_tone
    }