class PromptBuilder:
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
    
    GENDER_FACIAL_DETAILS = {
        "male": "balanced male face shape, firm jawline, defined brow ridge, masculine bone structure",
        "female": "soft facial structure, smooth jawline, gentle cheek volume, large expressive eyes"
    }
    
    GENDER_FACIAL_DETAILS_BEAR = {
        "male": (
            "exceptionally broad male face, heavy square jawline with blunt angles, "
            "substantial cheek mass and facial volume, strong prominent brow ridge, visible facial hair shadow"
        ),
        "female": (
            "broader than typical female face structure, strong defined jawline, fuller cheek volume"
        )
    }

    EYELIDS = {
        "monolid": (
            "IMPORTANT: authentic Korean monolid eyes, flat smooth upper eyelids, "
            "no visible eyelid crease at all, single eyelid, NOT double eyelid, NOT eyelid fold"
        ),
        "double": (
            "IMPORTANT: natural Korean double eyelids, clearly visible eyelid crease, "
            "defined but not deep-set eyelid fold, distinct outer fold line above the eye, NOT monolid"
        )
    }

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

    HAIRSTYLE_STYLES = {
        "puppy_male": "textured hair with bangs covering forehead",
        "dinosaur_male": "textured hair with bangs, energetic style",
        "fox_male": "sleek hair, refined style",
        "bear_male": "natural voluminous hair",
        "puppy_female": "soft bangs, bouncy texture",
        "cat_female": "no bangs, sleek straight hair, center-parted",
        "deer_female": "no bangs, flowing waves",
        "rabbit_female": "no bangs, light waves"
    }

    HAIRSTYLE_LENGTHS = {
        "long": "long flowing hair past shoulders, (rugged masculine long hair if male, NOT feminine)",
        "short-bob": "medium-length leaf cut or stylish bob reaching the chin, covering ears",
        "short": (
            "neat short cropped hair, with soft bangs covering the forehead, "
            "Korean dandy cut style, natural textured hair falling over eyebrows"
        )
    }

    FACE_SHAPES = {
        "v-line": "defined V-line jawline, gently tapered chin",
        "round": "soft round face shape, gentle curves"
    }

    CLOTHING = {
        "male": {"hoodie": "casual hoodie", "shirt": "clean shirt", "knit": "knit sweater"},
        "female": {"hoodie": "elegant hoodie", "shirt": "feminine shirt", "knit": "cozy knit"}
    }

    @staticmethod
    def get_skintone(value: int) -> str:
        if 0 <= value <= 25: return "very fair porcelain skin, MAC shade 13"
        elif 26 <= value <= 50: return "fair light skin, MAC shade 21"
        elif 51 <= value <= 75: return "medium natural skin, MAC shade 23"
        else: return "warm tan skin, MAC shade 28"

    @staticmethod
    def build_prompt(gender: str, animal: str, eyelid: str, face_shape: str,
                     hairstyle: str, clothing: str, makeup: str, skintone: int):
        
        parts = []
        
        # 1. Base
        if animal == "bear":
            parts.append(PromptBuilder.COMMON_BASE_BEAR)
        else:
            parts.append(PromptBuilder.COMMON_BASE)
        
        # 2. Gender Core
        parts.append(PromptBuilder.GENDER_CORE[gender])
        if gender == "male" and hairstyle == "long":
            parts.append("MAN WITH LONG HAIR, MASCULINE FACIAL STRUCTURE, THIS IS A MAN, NOT A WOMAN")

        # 3. Facial Details
        if animal == "bear":
            parts.append(PromptBuilder.GENDER_FACIAL_DETAILS_BEAR[gender])
        else:
            parts.append(PromptBuilder.GENDER_FACIAL_DETAILS[gender])

        # 4. Core Features
        parts.append(PromptBuilder.EYELIDS[eyelid])
        parts.append(PromptBuilder.ANIMAL_FACES[gender][animal])

        # 5. Styling
        parts.append(PromptBuilder.HAIRSTYLE_LENGTHS[hairstyle])
        parts.append(PromptBuilder.HAIRSTYLE_STYLES.get(f"{animal}_{gender}", "natural hair"))
        parts.append(PromptBuilder.FACE_SHAPES[face_shape])
        parts.append(PromptBuilder.get_skintone(skintone))
        
        clothing_desc = PromptBuilder.CLOTHING[gender][clothing]
        parts.append(f"wearing {clothing_desc}")
        
        parts.append("high dynamic range, natural color grading, realistic contrast")

        final_prompt = ", ".join(parts)
        
        # 6. Negative
        neg_parts = [
            "profile view, side view, looking away, illustration, anime, cartoon, CGI, 3D render",
            "over-smoothed skin, beauty filter, western facial features, extra fingers",
            f"female, woman, feminine, breasts" if gender == "male" else "male, man, masculine"
        ]
        if gender == "male" and hairstyle == "long":
            neg_parts.append("curvy body, feminine eyes, lipstick, makeup")
            
        final_negative = ", ".join(neg_parts)

        # 리턴값을 3개로 조정 (tokens를 마지막에 배치)
        return final_prompt, final_negative, len(final_prompt.split())
