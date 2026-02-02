class PromptBuilder:
    """
    FLUX.1-dev 성별/동물상 최적화 프롬프트 빌더 (통합본)
    구조: Common Base(정면 응시) + Gender Core(장발 보정) + Facial Details + Eyelids + Animal Face + Details
    """
    
    # ========== COMMON BASE (정면 응시 추가 및 곰상 체격 분리) ==========
    COMMON_BASE = (
        "A photorealistic studio portrait photograph, front facing, looking at camera, "
        "Korean subject in early 20s, natural proportions, balanced facial structure, "
        "realistic skin texture with visible pores, soft but directional studio lighting, "
        "85mm lens look, shallow depth of field, high detail, ultra realistic, "
        "cinematic color grading, professional photography quality"
    )
    
    COMMON_BASE_BEAR = (
        "A photorealistic studio portrait photograph, front facing, looking at camera, "
        "Korean subject in early 20s with atypically robust and heavy facial proportions, "
        "unusually wide and square facial structure, robust bone structure, "
        "thick neck and broad shoulders clearly visible in frame, "
        "realistic skin texture with visible pores, soft but directional studio lighting, "
        "50mm lens look, shallow depth of field, high detail, ultra realistic, "
        "cinematic color grading, professional photography quality"
    )
    
    # ========== GENDER CORE ==========
    GENDER_CORE = {
        "male": (
            "male, man, Korean young man, clearly male subject, unmistakably male appearance, "
            "this is a man, not a woman, masculine facial features"
        ),
        "female": (
            "female, woman, Korean young woman, clearly female subject, unmistakably female appearance, "
            "this is a woman, not a man"
        )
    }
    
    # ========== GENDER FACIAL DETAILS ==========
    GENDER_FACIAL_DETAILS = {
        "male": (
            "balanced male face shape, firm jawline without sharp V-line, "
            "subtle cheek volume typical of Korean men, defined brow ridge, "
            "slightly narrower lips, masculine bone structure"
        ),
        "female": (
            "soft facial structure, smooth jawline, gentle cheek volume, "
            "large expressive eyes, naturally full lips"
        )
    }
    
    GENDER_FACIAL_DETAILS_BEAR = {
        "male": (
            "exceptionally broad male face, heavy square jawline with blunt angles, "
            "substantial cheek mass and facial volume, strong prominent brow ridge, "
            "fuller lips proportional to large face, visible facial hair shadow"
        ),
        "female": (
            "broader than typical female face structure, strong defined jawline, "
            "fuller cheek volume, large expressive eyes, naturally full lips"
        )
    }
    
    # ========== GENDER NEGATIVE PROMPTS ==========
    GENDER_NEGATIVE = {
        "male": "female, woman, feminine face, girlish features, breasts, curvy body, soft makeup, lipstick",
        "female": "male, man, masculine face, facial hair, beard, mustache, strong brow ridge"
    }
    
    # ========== COMMON NEGATIVE (성별 무관) ==========
    COMMON_NEGATIVE = (
        "anime, illustration, cartoon, CGI, 3D render, over-smoothed skin, beauty filter, plastic skin, "
        "western facial features, caucasian, Japanese style, j-pop idol, exaggerated eyes, "
        "extra fingers, distorted face, artificial lighting, overexposed, face swap"
    )
    
    # ========== 눈꺼풀 (NOT logic 포함) ==========
    EYELIDS = {
        "monolid": (
            "IMPORTANT: authentic Korean monolid eyes, flat smooth upper eyelids, "
            "no visible eyelid crease at all, single eyelid with uninterrupted lid surface, "
            "NOT double eyelid, NOT eyelid fold, NOT outer crease"
        ),
        "double": (
            "IMPORTANT: natural Korean double eyelids, clearly visible eyelid crease while eyes are open, "
            "defined but not deep-set eyelid fold, distinct outer fold line above the eye, NOT monolid"
        )
    }
    
    # ========== 동물상 (곰상 최종 개선) ==========
    ANIMAL_FACES = {
        "female": {
            "puppy": "round eyes with slightly drooping outer corners, visible aegyo-sal, gentle smile, friendly impression",
            "cat": "almond-shaped eyes with upturned outer corners, mysterious aura, neutral expression, sharp focused gaze",
            "deer": "bright sparkling eyes, warm and gentle gaze, innocent look, tender expression",
            "rabbit": "round eyes with big dark pupils, petite nose and mouth, gentle smile showing front teeth"
        },
        "male": {
            "puppy": "round eyes with slightly drooping outer corners, visible aegyo-sal, gentle smile, friendly youthful charm",
            "dinosaur": "strong presence, bold prominent facial features, wide natural smile, boyish energetic charm, charismatic gaze",
            "fox": "sharp elongated eyes with raised outer corners, sleek angular facial contours, straight defined nose bridge, thin lips",
            "bear": "exceptionally wide and square face, heavy facial volume, thick neck visually connected to jaw, broad sturdy shoulders"
        }
    }
    
    # ========== 헤어스타일 (남성 장발 보정 포함) ==========
    HAIRSTYLE_STYLES = {
        "puppy_male": "textured hair with bangs covering forehead, slight natural waves",
        "dinosaur_male": "textured hair with bangs, slight thick natural waves",
        "bear_male": "natural voluminous hair with bangs",
        "fox_male": "sleek straight hair combed back, refined masculine style",
        "puppy_female": "soft bangs, slight thick waves, bouncy texture",
        "cat_female": "no bangs, sleek straight hair, center-parted",
        "deer_female": "no bangs, gentle waves, soft flowing style",
        "rabbit_female": "no bangs, light waves, natural feminine fall"
    }
    
    HAIRSTYLE_LENGTHS = {
        "long": {
            "male": "EXTREMELY LONG HAIR reaching middle of back, masculine long hair on a man, rugged male locks, NOT FEMININE",
            "female": "very long flowing hair past shoulders"
        },
        "short-bob": {
            "male": "medium-length leaf cut, chin length, trendy Korean male bob silhouette, masculine cut",
            "female": "short bob haircut at chin length"
        },
        "short": {
            "male": "short cropped hair, clean faded sides, neat masculine short cut",
            "female": "short cropped hair above ears"
        }
    }
    
    FACE_SHAPES = {
        "v-line": "defined V-line jawline, gently tapered chin",
        "round": "soft round face shape, gentle curves"
    }
    
    CLOTHING = {
        "male": {"hoodie": "wearing a clean casual hoodie", "shirt": "wearing a clean casual shirt", "knit": "wearing a casual knit sweater"},
        "female": {"hoodie": "wearing a simple elegant hoodie", "shirt": "wearing a clean feminine shirt", "knit": "wearing a cozy elegant knit sweater"}
    }
    
    QUALITY_KEYWORDS = "high dynamic range, natural color grading, realistic contrast"
    
    @staticmethod
    def get_skintone(value: int) -> str:
        if 0 <= value <= 25: return "very fair porcelain skin, MAC shade 13"
        elif 26 <= value <= 50: return "fair light skin, MAC shade 21"
        elif 51 <= value <= 75: return "medium natural skin, MAC shade 23"
        else: return "warm tan skin, MAC shade 28"
    
    @staticmethod
    def get_styling(gender: str, animal: str, intensity: str) -> str:
        if gender == "male":
            return "no visible makeup, natural lips with no lip product, clean natural appearance"
        else:
            if intensity == "light":
                return "light natural makeup, soft blush, clear lip balm"
            else:
                return "bold makeup, sharp winged eyeliner, deep lipstick color"

    @staticmethod
    def build_prompt(gender: str, animal: str, eyelid: str, face_shape: str,
                     hairstyle: str, clothing: str, makeup: str, skintone: int):
        
        parts = []
        
        # 1. Base (곰상 여부 반영 + 정면 응시)
        parts.append(PromptBuilder.COMMON_BASE_BEAR if animal == "bear" else PromptBuilder.COMMON_BASE)
        
        # 2. Gender Core (장발 시 남성성 재강조)
        parts.append(PromptBuilder.GENDER_CORE[gender])
        if gender == "male" and hairstyle == "long":
            parts.append("MAN WITH LONG HAIR, MASCULINE FACIAL STRUCTURE, THIS IS A MAN, NOT A WOMAN")
        
        # 3. Facial Details
        if animal == "bear":
            parts.append(PromptBuilder.GENDER_FACIAL_DETAILS_BEAR[gender])
        else:
            parts.append(PromptBuilder.GENDER_FACIAL_DETAILS[gender])
        
        # 4. Features (눈꺼풀, 동물상)
        parts.append(PromptBuilder.EYELIDS[eyelid])
        parts.append(PromptBuilder.ANIMAL_FACES[gender][animal])
        
        # 5. Styling
        parts.append(PromptBuilder.get_styling(gender, animal, makeup))
        parts.append(PromptBuilder.HAIRSTYLE_LENGTHS[hairstyle][gender])
        parts.append(PromptBuilder.HAIRSTYLE_STYLES.get(f"{animal}_{gender}", "natural hair"))
        parts.append(PromptBuilder.FACE_SHAPES[face_shape])
        parts.append(PromptBuilder.get_skintone(skintone))
        parts.append(PromptBuilder.CLOTHING[gender][clothing])
        parts.append(PromptBuilder.QUALITY_KEYWORDS)
        
        final_prompt = ", ".join(parts)
        
        # 6. Negative (여성화 방지 로직 포함)
        eyelid_neg = ", monolid eyes" if eyelid == "double" else ", double eyelids"
        bear_neg = ", slim face, thin neck" if animal == "bear" else ""
        gender_neg = PromptBuilder.GENDER_NEGATIVE[gender]
        
        final_negative = f"{PromptBuilder.COMMON_NEGATIVE}, {gender_neg}{eyelid_neg}{bear_neg}"
        
        # 7. 요약 및 토큰
        animal_kor = {"puppy": "강아지상", "cat": "고양이상", "deer": "사슴상", "rabbit": "토끼상", "dinosaur": "공룡상", "fox": "여우상", "bear": "곰상"}
        gender_kor = {"male": "남성", "female": "여성"}
        korean_summary = f"{gender_kor[gender]}_{animal_kor[animal]}"

        return final_prompt, final_negative, korean_summary, len(final_prompt.split())
