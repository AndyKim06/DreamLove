# ============================================
# [FLUX.1-dev 최적화] 이상형 프롬프트 엔진 최종본 (Ver 6.5 최종)
# ============================================

# 분위기
MOOD_MAP = {
    "청순": "innocent pure aura, serene expression, gentle smile, wavy hair",
    "시크": "sophisticated cool vibe, confident gaze, sharp features, high nose bridge, closed lips, sleek straight hair",
    "귀여운": "adorable playful mood, cheerful expression, subtle aegyo-sal, cheerful smile, curly hair"
}

# 얼굴형
FACE_SHAPE_MAP = {
    "둥근형": "round face, full cheeks, smooth jawline",
    "V라인": "sharp V-line chin, high cheekbones, slim face"
}

# 쌍커풀
EYELID_MAP = {
    "무쌍": {
        "청순": "monolid single eyelid, gentle rounded shape, serene gaze, absolutely no crease, no fold",
        "시크": "monolid single eyelid, sharp horizontal line, intense gaze, absolutely no crease, no fold",
        "귀여운": "monolid single eyelid, round bright eyes, absolutely no crease, no fold"
    },
    "겉쌍": "prominent double eyelids, wide folds, parallel creases"
}

# 헤어스타일
HAIR_MAP = {
    "긴머리": "long hair",
    "단발": "bob cut",
    "숏컷": "short hair"
}

# 의상
CLOTHING_MAP = {
    "셔츠": "white collared shirt",
    "니트": "beige knit sweater",
    "후드티": "gray casual hoodie"
}

# 시각적 품질
VISUAL_QUALITY = "upper body portrait, professional photo, white background"

# 피부톤 변환 함수
def get_skin_tone(value):
    if value <= 0.25:
        return "fair porcelain skin, luminous"
    elif value <= 0.5:
        return "bright ivory skin, clear complexion"
    elif value <= 0.75:
        return "natural beige skin, youthful"
    else:
        return "sun-kissed tan skin, youthful"

# ============================================
# 여성 전용
# ============================================

FEMALE_BASE = "beautiful 20-year-old Korean woman, flawless skin, delicate features"

MAKEUP_FEMALE = {
    "연하게": "natural dewy skin, soft pink lips, minimal eye makeup",
    "진하게": "K-pop idol makeup, cat-eye liner, dramatic extended lashes, thick mascara, gradient coral lips, glass skin"
}

def build_prompt_female(mood, face_shape, eyelid, hair, clothing, makeup, skin_tone_value):
    if eyelid == "무쌍":
        eyelid_prompt = EYELID_MAP["무쌍"][mood]
    else:
        eyelid_prompt = EYELID_MAP[eyelid]
    
    prompt_parts = [
        FEMALE_BASE,
        get_skin_tone(skin_tone_value),
        eyelid_prompt,
        FACE_SHAPE_MAP[face_shape],
        MOOD_MAP[mood],
        HAIR_MAP[hair],
        CLOTHING_MAP[clothing],
        MAKEUP_FEMALE[makeup],
        VISUAL_QUALITY
    ]
    
    return ", ".join(prompt_parts)

# ============================================
# 남성 전용
# ============================================

MALE_BASE = "handsome 20-year-old Korean man, flawless skin, delicate features"

GROOMING_MALE = {
    "연하게": "natural",
    "진하게": "defined brows"
}

def build_prompt_male(mood, face_shape, eyelid, hair, clothing, grooming, skin_tone_value):
    if eyelid == "무쌍":
        eyelid_prompt = EYELID_MAP["무쌍"][mood]
    else:
        eyelid_prompt = EYELID_MAP[eyelid]
    
    prompt_parts = [
        MALE_BASE,
        get_skin_tone(skin_tone_value),
        eyelid_prompt,
        FACE_SHAPE_MAP[face_shape],
        MOOD_MAP[mood],
        HAIR_MAP[hair],
        CLOTHING_MAP[clothing],
        GROOMING_MALE[grooming],
        VISUAL_QUALITY
    ]
    
    return ", ".join(prompt_parts)

# ============================================
# 통합 인터페이스
# ============================================

def build_prompt(gender, mood, face_shape, eyelid, hair, clothing, makeup, skin_tone_value):
    if gender == "여성":
        return build_prompt_female(
            mood=mood,
            face_shape=face_shape,
            eyelid=eyelid,
            hair=hair,
            clothing=clothing,
            makeup=makeup,
            skin_tone_value=skin_tone_value
        )
    else:
        return build_prompt_male(
            mood=mood,
            face_shape=face_shape,
            eyelid=eyelid,
            hair=hair,
            clothing=clothing,
            grooming=makeup,
            skin_tone_value=skin_tone_value
        )