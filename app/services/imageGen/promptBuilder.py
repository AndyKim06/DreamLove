class PromptBuilder:
    """
    FLUX.1-dev 성별 분기 프롬프트 빌더
    구조: Common Base + Gender Branch + Eyelids(우선) + Animal Face + Details
    """
    
    # ========== COMMON BASE (성별 무관 공통 - neutral expression 제거) ==========
    COMMON_BASE = (
        "A photorealistic studio portrait photograph, "
        "Korean subject in early 20s, "
        "natural proportions, "
        "balanced facial structure, "
        "realistic skin texture with visible pores, "
        "soft but directional studio lighting, "
        "85mm lens look, shallow depth of field, "
        "high detail, ultra realistic, "
        "cinematic color grading, "
        "professional photography quality"
    )
    
    # ========== COMMON BASE FOR BEAR (곰상 전용) ==========
    COMMON_BASE_BEAR = (
        "A photorealistic studio portrait photograph, "
        "Korean subject in early 20s with atypically robust and heavy facial proportions, "
        "unusually wide and square facial structure, "
        "robust bone structure, "
        "thick neck and broad shoulders clearly visible in frame, "
        "realistic skin texture with visible pores, "
        "soft but directional studio lighting, "
        "50mm lens look, shallow depth of field, "
        "high detail, ultra realistic, "
        "cinematic color grading, "
        "professional photography quality"
    )
    
    # ========== GENDER CORE ==========
    GENDER_CORE = {
        "male": (
            "male, man, Korean young man, "
            "clearly male subject, unmistakably male appearance, "
            "this is a man, not a woman"
        ),
        "female": (
            "female, woman, Korean young woman, "
            "clearly female subject, unmistakably female appearance, "
            "this is a woman, not a man"
        )
    }
    
    # ========== GENDER FACIAL DETAILS ==========
    GENDER_FACIAL_DETAILS = {
        "male": (
            "balanced male face shape, "
            "firm jawline without sharp V-line, "
            "subtle cheek volume typical of Korean men, "
            "defined brow ridge, "
            "slightly narrower lips, "
            "subtle facial hair shadow"
        ),
        "female": (
            "soft facial structure, "
            "smooth jawline, "
            "gentle cheek volume, "
            "large expressive eyes, "
            "naturally full lips"
        )
    }
    
    # ========== GENDER FACIAL DETAILS FOR BEAR (곰상 전용) ==========
    GENDER_FACIAL_DETAILS_BEAR = {
        "male": (
            "exceptionally broad male face, "
            "heavy square jawline with blunt angles, "
            "substantial cheek mass and facial volume, "
            "strong prominent brow ridge, "
            "fuller lips proportional to large face, "
            "visible facial hair shadow"
        ),
        "female": (
            "broader than typical female face structure, "
            "strong defined jawline, "
            "fuller cheek volume, "
            "large expressive eyes, "
            "naturally full lips"
        )
    }
    
    # ========== GENDER NEGATIVE PROMPTS ==========
    GENDER_NEGATIVE = {
        "male": (
            "female, woman, feminine face, girlish features, "
            "soft makeup, lipstick, blush, eyeliner, "
            "cute, pretty girl"
        ),
        "female": (
            "male, man, masculine face, "
            "facial hair, beard, mustache, "
            "strong brow ridge"
        )
    }
    
    # ========== COMMON NEGATIVE (성별 무관) ==========
    COMMON_NEGATIVE = (
        "anime, illustration, cartoon, CGI, 3D render, "
        "over-smoothed skin, beauty filter, plastic skin, "
        "western facial features, caucasian, "
        "Japanese facial features, Japanese style, j-pop idol, anime-inspired beauty, "
        "exaggerated eyes, unreal proportions, "
        "extra fingers, distorted face, asymmetry, "
        "artificial lighting, overexposed, "
        "glossy skin, porcelain doll, "
        "face swap, identity mixing, look-alike artifact"
    )
    
    # ========== 눈꺼풀 ==========
    EYELIDS = {
        "monolid": (
            "IMPORTANT: authentic Korean monolid eyes, "
            "flat smooth upper eyelids, "
            "no visible eyelid crease at all, "
            "single eyelid with uninterrupted lid surface, "
            "NOT double eyelid, NOT eyelid fold, NOT outer crease, "
            "natural Korean monolid eye anatomy"
        ),
        "double": (
            "IMPORTANT: natural Korean double eyelids, "
            "clearly visible eyelid crease while eyes are open, "
            "defined but not deep-set eyelid fold, "
            "parallel or in-out double eyelid style common in Korea, "
            "distinct outer fold line above the eye, "
            "NOT monolid, NOT single eyelid, NOT flat eyelid, "
            "typical Korean double eyelid appearance"
        )
    }
    
    # ========== 동물상 (성별별, 곰상 최종 개선) ==========
    ANIMAL_FACES = {
        "female": {
            "puppy": (
                "moderately sized round eyes with slightly drooping outer corners, "
                "natural eye size proportional to face, "
                "visible aegyo-sal under eyes, "
                "gentle subtle smile without showing teeth, "
                "cute and friendly impression, warm gaze"
            ),
            "cat": (
                "moderately sized almond-shaped eyes with upturned outer corners, "
                "natural eye size proportional to face, "
                "cold and mysterious aura, sophisticated vibe, "
                "neutral expression, no smile, relaxed lips, "
                "sharp focused gaze"
            ),
            "deer": (
                "bright sparkling eyes, natural eye size proportional to face, "
                "warm and gentle gaze, "
                "innocent look, soft smile without showing teeth, "
                "tender expression"
            ),
            "rabbit": (
                "round chubby feminine face, "
                "moderately sized round eyes with big dark pupils, "
                "natural eye size proportional to face, "
                "small delicate face, petite nose and mouth, "
                "gentle smile with slight front teeth showing, slightly protruding incisors, "
                "soft cheerful expression"
            )
        },
        "male": {
            "puppy": (
                "moderately sized round eyes with slightly drooping outer corners, "
                "natural eye size proportional to face, "
                "visible aegyo-sal under eyes, "
                "gentle subtle smile without showing teeth, "
                "friendly impression, warm gaze"
            ),
            "dinosaur": (
                "IMPORTANT: expressive playful energetic facial expression, "
                "wide natural smile clearly showing upper front teeth, "
                "slightly wider nose with clearly visible nostrils, "
                "bold prominent facial features, "
                "boyish energetic charm, "
                "friendly lively vibe, "
                "natural eye size proportional to face"
            ),
            "fox": (
                "sharp elongated eyes with raised outer corners, "
                "natural eye size proportional to face, "
                "thinly arched eyebrows angled upward, "
                "sleek angular facial contours, straight defined nose bridge, "
                "thin lips, sharp jawline, charismatic gaze"
            ),
            "bear": (
                "IMPORTANT: exceptionally wide and square face, "
                "face width noticeably larger than average Korean proportions, "
                "heavy prominent facial bone structure, "
                "full cheeks with visible facial volume and mass, "
                "face occupying a large portion of the frame, "
                "proportionally thick neck, neck width approaching jawline width, "
                "neck and jaw visually connected without sharp separation, "
                "broad sturdy shoulders clearly visible in frame, "
                "strong square jaw with blunt angles, "
                "calm but imposing presence, dependable and protective aura, "
                "bold thick eyebrows, prominent straight nose bridge, "
                "natural eye size proportional to face"
            )
        }
    }
    
    # ========== 헤어스타일 스타일 맵 ==========
    HAIRSTYLE_STYLES = {
        # 남성
        "puppy_male": "short to medium-length hair with bangs covering forehead, slight natural waves, voluminous texture",
        "dinosaur_male": "short to medium-length hair with bangs, slight thick natural waves, textured casual style",
        "bear_male": "short to medium-length hair with bangs, natural waves, full hair",
        "fox_male": "short to medium-length hair, no bangs, sleek straight hair combed back, refined masculine style",
        
        # 여성
        "puppy_female": "soft bangs covering forehead, slight thick waves, bouncy feminine texture",
        "cat_female": "no bangs, sleek straight hair, center-parted, polished elegant look",
        "deer_female": "no bangs, gentle waves, warm brown hair, soft flowing feminine style",
        "rabbit_female": "no bangs, light waves, warm brown hair, natural feminine fall"
    }
    
    HAIRSTYLE_LENGTHS = {
        "long": "long hair flowing past shoulders",
        "short-bob": "short bob haircut at chin length",
        "short": "short cropped hair above ears"
    }
    
    # ========== 얼굴형 ==========
    FACE_SHAPES = {
        "v-line": "defined V-line jawline, gently tapered chin, balanced face shape",
        "round": "soft round face shape, gentle curved jawline, fuller cheeks"
    }
    
    # ========== 옷 (성별별) ==========
    CLOTHING = {
        "male": {
            "hoodie": "wearing a clean casual hoodie",
            "shirt": "wearing a clean casual shirt",
            "knit": "wearing a casual knit sweater"
        },
        "female": {
            "hoodie": "wearing a simple elegant hoodie",
            "shirt": "wearing a clean feminine shirt",
            "knit": "wearing a cozy elegant knit sweater"
        }
    }
    
    # ========== 품질 키워드 ==========
    QUALITY_KEYWORDS = "high dynamic range, natural color grading, realistic contrast"
    
    # ========== 피부톤 (4단계) ==========
    @staticmethod
    def get_skintone(value: int) -> str:
        """0-100 값을 4단계 피부톤으로 변환 (MAC 기준)"""
        if 0 <= value <= 25:
            return "very fair porcelain skin tone, MAC shade 13, pale complexion with cool undertones"
        elif 26 <= value <= 50:
            return "fair light skin tone, MAC shade 21, bright complexion with neutral undertones"
        elif 51 <= value <= 75:
            return "medium natural skin tone, MAC shade 23, typical Korean complexion with warm undertones"
        else:  # 76-100
            return "warm tan skin tone, MAC shade 28, sun-kissed complexion with golden undertones"
    
    # ========== 메이크업/스타일링 (성별별) ==========
    @staticmethod
    def get_styling(gender: str, animal: str, intensity: str) -> str:
        """성별 + 동물상 + 강도에 따른 스타일링"""
        
        if gender == "male":
            if intensity == "light":
                return "no visible makeup, natural lips with no lip product, clean natural appearance"
            else:  # heavy
                return "minimal grooming with matte finish, very subtle contouring, no lip product"
        
        else:  # female
            if animal == "cat":
                if intensity == "light":
                    return "light natural makeup, soft contouring, clear lip balm or subtle gloss, defined eyeshadow and thin eyeliner"
                else:  # heavy
                    return "bold makeup with long dramatic eyelashes, smoky eyeshadow, sharp winged eyeliner, deep lipstick color"
            
            else:  # puppy, deer, rabbit
                if intensity == "light":
                    return "soft natural makeup with light blush, clear lip balm or subtle gloss, minimal eye makeup"
                else:  # heavy
                    return "enhanced makeup with natural-looking eyelashes, soft eyeshadow, rosy blush, deeper lip color"
    
    # ========== 헤어스타일 조합 ==========
    @staticmethod
    def get_hairstyle(gender: str, animal: str, length: str) -> str:
        """동물상별 스타일 + 길이"""
        style_key = f"{animal}_{gender}"
        style = PromptBuilder.HAIRSTYLE_STYLES.get(style_key, "natural styled hair")
        length_desc = PromptBuilder.HAIRSTYLE_LENGTHS[length]
        return f"{length_desc}, {style}"
    
    # ========== 최종 프롬프트 빌드 ==========
    @staticmethod
    def build_prompt(gender: str, animal: str, eyelid: str, face_shape: str,
                     hairstyle: str, clothing: str, makeup: str, skintone: int):
        """
        FLUX.1-dev 성별 분기 프롬프트 빌더
        
        구조 (순서 개선):
        1. COMMON BASE (곰상 선택 시 특수 버전 사용)
        2. GENDER CORE (성별 명시 3회+)
        3. GENDER FACIAL DETAILS (곰상 선택 시 특수 버전 사용)
        4. 눈꺼풀 (우선 배치!)
        5. 동물상 특징 (공룡상 표정 강화, 곰상 최종 개선)
        6. 스타일링 (메이크업/그루밍)
        7. 헤어스타일
        8. 얼굴형
        9. 피부톤
        10. 옷 (성별별)
        11. 품질 키워드
        
        Returns: (영문 프롬프트, 네거티브 프롬프트, 한글 요약, 토큰 수)
        """
        
        parts = []
        
        # 1. COMMON BASE (곰상 선택 시 특수 버전)
        if animal == "bear":
            parts.append(PromptBuilder.COMMON_BASE_BEAR)
        else:
            parts.append(PromptBuilder.COMMON_BASE)
        
        # 2. GENDER CORE (최우선!)
        parts.append(PromptBuilder.GENDER_CORE[gender])
        
        # 3. GENDER FACIAL DETAILS (곰상 선택 시 특수 버전)
        if animal == "bear":
            parts.append(PromptBuilder.GENDER_FACIAL_DETAILS_BEAR[gender])
        else:
            parts.append(PromptBuilder.GENDER_FACIAL_DETAILS[gender])
        
        # 4. 눈꺼풀 (우선 배치!)
        parts.append(PromptBuilder.EYELIDS[eyelid])
        
        # 5. 동물상
        parts.append(PromptBuilder.ANIMAL_FACES[gender][animal])
        
        # 6. 스타일링
        parts.append(PromptBuilder.get_styling(gender, animal, makeup))
        
        # 7. 헤어스타일
        parts.append(PromptBuilder.get_hairstyle(gender, animal, hairstyle))
        
        # 8. 얼굴형
        parts.append(PromptBuilder.FACE_SHAPES[face_shape])
        
        # 9. 피부톤
        parts.append(PromptBuilder.get_skintone(skintone))
        
        # 10. 옷 (성별별)
        parts.append(PromptBuilder.CLOTHING[gender][clothing])
        
        # 11. 품질 키워드
        parts.append(PromptBuilder.QUALITY_KEYWORDS)
        
        # 최종 조합
        final_prompt = ", ".join(parts)
        
        # NEGATIVE 조합 (COMMON + GENDER + 눈꺼풀 조건부 + 곰상 조건부)
        eyelid_negative = ""
        if eyelid == "double":
            eyelid_negative = ", monolid eyes, single eyelid, flat eyelids, no eyelid crease, hidden eyelid fold, hooded eyes, barely visible eyelid line"
        elif eyelid == "monolid":
            eyelid_negative = ", double eyelids, eyelid crease, outer fold, inner fold, visible eyelid line, Western-style eyes"
        
        # 곰상 네거티브 추가
        bear_negative = ""
        if animal == "bear":
            bear_negative = ", slim face, narrow face, thin face, V-line jawline, pointed chin, thin neck, slender neck, delicate features, soft jawline, small face"
        
        final_negative = f"{PromptBuilder.COMMON_NEGATIVE}, {PromptBuilder.GENDER_NEGATIVE[gender]}{eyelid_negative}{bear_negative}"
        
        # 토큰 계산
        tokens = len(final_prompt.split())
        
        return final_prompt, final_negative, tokens