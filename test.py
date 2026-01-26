import os
import random
from datetime import datetime
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import re

# .env 파일에서 API 토큰 불러오기
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Hugging Face Inference Client 초기화
client = InferenceClient(token=HF_TOKEN)

# === 이상형 페르소나 프리셋 - 동물상 7종 + 분위기 3종 (축약) ===
STYLE_PRESETS = {
    # === 동물상 (7가지) - 핵심만 ===
    
    "강아지상": "drooping eye corners, round eyes, soft face, innocent gaze, friendly smile",
    "고양이상": "upturned eye corners, sharp V-line face, aloof gaze, sophisticated",
    "뱀상": "long horizontal eyes, exotic features, seductive gaze, glamorous",
    "사슴상": "large soulful eyes, slender neck, elegant features, pure aura",
    "곰상": "kind gentle eyes, sturdy build, trustworthy, comforting aura",
    "늑대상": "intense eyes, sharp jawline, strong structure, fierce charismatic",
    "토끼상": "bright round eyes, plump cheeks, adorable lively, playful charm",
    
    # === 분위기 스타일 (축약) ===
    
    "청순한": "pale skin, innocent gaze, minimal makeup, pure atmosphere",
    "시크한": "sharp features, confident expression, sophisticated style, cool lighting",
    "귀여운": "bright eyes, playful expression, youthful energy, adorable presence",
    
    # === 눈꺼풀 관련 (축약) ===
    
    "쌍꺼풀": "double eyelids, defined crease",
    "무쌍": "monolid, flat eyelid, no crease, smooth eyelid",
    "속쌍": "inner double eyelid, subtle crease",
}

# === 키워드 별칭 ===
KEYWORD_ALIASES = {
    "강아지상": ["강아지", "puppy"],
    "고양이상": ["고양이", "cat"],
    "뱀상": ["뱀", "snake"],
    "사슴상": ["사슴", "deer"],
    "곰상": ["곰", "bear"],
    "늑대상": ["늑대", "wolf"],
    "토끼상": ["토끼", "rabbit"],
    "청순한": ["청순", "pure"],
    "시크한": ["시크", "chic"],
    "귀여운": ["귀여", "cute"],
    "쌍꺼풀": ["쌍커풀", "쌍거풀"],
    "무쌍": ["무쌍커풀"],
    "속쌍": ["속쌍커풀"],
}

def expand_style_preset(user_prompt):
    """
    사용자 프롬프트에 스타일 키워드가 있으면 확장 (간결하게)
    """
    expanded_prompt = user_prompt
    detected_keywords = []
    
    # 1. 정확한 키워드 매칭
    for style_key, expansion in STYLE_PRESETS.items():
        if style_key in expanded_prompt:
            # 키워드를 확장된 텍스트로 교체
            expanded_prompt = expanded_prompt.replace(style_key, expansion)
            detected_keywords.append(style_key)
    
    # 2. 별칭 매칭
    for style_key, aliases in KEYWORD_ALIASES.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, expanded_prompt, re.IGNORECASE):
                if style_key not in detected_keywords:
                    expansion = STYLE_PRESETS[style_key]
                    expanded_prompt = f"{expanded_prompt}, {expansion}"
                    detected_keywords.append(style_key)
                    break
    
    return expanded_prompt, detected_keywords

def generate_image(user_prompt, gender="female", prompt_version="long", seed=None):
    """
    사용자 프롬프트 + 한국인 이상형 기본 설정으로 이미지 생성
    
    Args:
        user_prompt (str): 사용자가 입력한 특징
        gender (str): "male" 또는 "female"
        prompt_version (str): "long" 또는 "short"
        seed (int): 고정 시드 (None이면 랜덤)
    
    Returns:
        tuple: (PIL.Image, int) - (생성된 이미지, 사용된 시드)
    """
    
    # 시드 관리
    if seed is None:
        seed = random.randint(0, 999999)
    
    # 스타일 프리셋 확장
    original_prompt = user_prompt
    user_prompt, detected_keywords = expand_style_preset(user_prompt)
    
    # 확장되었는지 확인
    if detected_keywords:
        print(f"   [INFO] 감지된 키워드: {', '.join(detected_keywords)}")
    
    # === 축약된 Visual Anchor ===
    visual_anchor = "soft lighting, flawless skin, porcelain texture, clear iris, symmetrical face"
    
    # === 축약된 Base 프롬프트 ===
    if gender == "male":
        base_prompt = """
        Korean man 20s, handsome attractive,
        clean-shaven smooth skin, no facial hair no beard no stubble,
        k-pop idol clear skin, flawless texture,
        high nose bridge, soft features, warm eyes,
        boyfriend material, approachable clean appearance
        """
    else:
        base_prompt = """
        Korean woman 20s, pretty attractive, girlfriend material,
        soft features, gentle V-line, warm sparkling eyes, bright smile,
        high nose bridge, elegant nose, flawless glowing skin,
        natural Korean makeup, approachable, lovely presence
        """
    
    # 프롬프트 조합 (간결하게)
    final_prompt = f"""
    {user_prompt}, {base_prompt}, {visual_anchor},
    upper body portrait, white background, front facing,
    professional photography, photorealistic, high quality
    """.strip()
    
    # 한 줄로 정리
    final_prompt = " ".join(final_prompt.split())
    
    # === 길이 체크 (2000자 제한) ===
    if len(final_prompt) > 2000:
        print(f"   [WARNING] 프롬프트 길이 초과 ({len(final_prompt)}자 > 2000자)")
        print(f"   [INFO] 자동 축약 중...")
        
        # Base 프롬프트 더 줄이기
        if gender == "male":
            base_prompt = "Korean man 20s, handsome, clean-shaven smooth skin, no beard, high nose, warm eyes"
        else:
            base_prompt = "Korean woman 20s, pretty, soft features, warm eyes, bright smile, high nose, flawless skin"
        
        visual_anchor = "soft lighting, flawless skin, clear face"
        
        final_prompt = f"{user_prompt}, {base_prompt}, {visual_anchor}, portrait, white background, photorealistic"
        final_prompt = " ".join(final_prompt.split())
        
        print(f"   [INFO] 축약 완료 ({len(final_prompt)}자)")
    
    try:
        print(f"   Seed: {seed}")
        
        # 기술적 파라미터 최적화
        image = client.text_to_image(
            prompt=final_prompt,
            model="black-forest-labs/FLUX.1-dev",
            width=768,
            height=1024,
        )
        
        return image, seed
        
    except Exception as e:
        print(f"   [ERROR] {e}")
        return None, seed

def save_image_with_timestamp(image, filename_base, index):
    """
    타임스탬프를 포함한 파일명으로 저장
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_base}_{timestamp}_{index}.png"
    image.save(filename)
    return filename

def quick_generate(user_prompt, gender="female", num_images=4):
    """
    빠른 생성 함수 (여러 장 생성, 자동 저장)
    
    Args:
        user_prompt (str): 사용자 프롬프트
        gender (str): "male" 또는 "female"
        num_images (int): 생성할 이미지 개수 (기본 4장)
    
    Returns:
        list: [(image, seed), ...] 형태의 리스트
    """
    print(f"\n{'='*80}")
    print(f"[IDEAL TYPE IMAGE GENERATION - {num_images} Images]")
    print(f"{'='*80}\n")
    
    print(f"[SETTINGS]")
    print(f"   Model: FLUX.1-dev")
    print(f"   Gender: {'Female' if gender == 'female' else 'Male'}")
    print(f"   Number of Images: {num_images}")
    print(f"   Original Input: {user_prompt}")
    print()
    
    results = []
    
    for i in range(num_images):
        print(f"[GENERATING] Image {i+1}/{num_images}")
        
        # 각 이미지마다 다른 랜덤 시드 사용
        image, seed = generate_image(user_prompt, gender=gender, prompt_version="long", seed=None)
        
        if image:
            filename = save_image_with_timestamp(image, f"ideal_{gender}", i+1)
            print(f"   ✓ Saved: {filename}")
            results.append((image, seed, filename))
        else:
            print(f"   ✗ Failed to generate image {i+1}")
            results.append((None, seed, None))
        
        print()
    
    # 최종 결과 요약
    print(f"{'='*80}")
    print(f"[SUMMARY]")
    success_count = sum(1 for r in results if r[0] is not None)
    print(f"   Success: {success_count}/{num_images}")
    print(f"   Seeds used: {[r[1] for r in results if r[0] is not None]}")
    print(f"{'='*80}\n")
    
    return results

# ============================================================================
# Generate Your Ideal Type Here
# ============================================================================

if __name__ == "__main__":
    
    # ========================================
    # Edit This Section
    # ========================================
    
    # Test: 자유로운 입력
    MY_PROMPT = "귀여운 곰상, 큰 눈에 무쌍, 높은 코, 도톰한 입술, 각있는 둥근얼굴, 포근한 인상"
    MY_GENDER = "male"
    NUM_IMAGES = 4  # 생성할 이미지 개수
    
    # ========================================
    # End of Edit Section
    # ========================================
    
    # Execute Generation
    quick_generate(MY_PROMPT, MY_GENDER, NUM_IMAGES)