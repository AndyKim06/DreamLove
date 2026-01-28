import os
import glob
import random
from huggingface_hub import InferenceClient
from app.core.config import settings

# Hugging Face 클라이언트 설정
client = InferenceClient(token=settings.FLUX_API_KEY)

# AI 최적화 동물상 매핑 사전 (해부학적 특징 보강)
ANIMAL_FEATURES = {
    "male": {
        "Type 1": "dinosaur-face shape, very sharp and strong square jawline, intense eyes",
        "Type 2": "wolf-face shape, cold chic eyes, high straight nose bridge, sharp look",
        "Type 3": "puppy-face shape, soft rounded eyes, friendly warm smile",
        "Type 4": "bear-face shape, clean and sturdy facial structure, gentle impression"
    },
    "female": {
        "Type 1": "cat-face shape, sharp upturned eye corners, slim V-line, sophisticated gaze",
        "Type 2": "puppy-face shape, drooping eye corners, soft jawline, innocent and clear eyes",
        "Type 3": "rabbit-face shape, bright round eyes, adorable lively expression, youthful",
        "Type 4": "deer-face shape, slender neck, large clear eyes, elegant calm aura"
    }
}

async def generate_ideal_image_logic(data):
    # 1. 기본 인물 및 피부톤 설정
    base = "Korean man" if data.gender == "male" else "Korean woman"
    animal = ANIMAL_FEATURES[data.gender][data.ref_type]
    skin_desc = "pale porcelain skin" if data.skin_tone < 50 else "natural tanned sun-kissed skin"
    
    # 2. 증명사진 구도 및 실사 퀄리티 프롬프트 강화
    # 정면 응시, 상반신 고정, 모공 및 실제 피부 질감 강조
    composition = "center-aligned, passport photo style, front view, looking at camera, head and shoulders shot"
    realism_boost = "highly detailed skin texture, visible fine pores, natural skin oils, matte skin, no plastic look, authentic human skin, extremely realistic"
    lighting = "soft studio lighting, neutral solid grey background, professional photography"

    prompt = (
        f"{composition}, a photorealistic {base}, {animal}, "
        f"{data.eyelid} eyes, {data.hair} hair, {data.face_shape} face shape, "
        f"wearing {data.outfit}, {data.makeup} makeup, {data.mood} atmosphere, "
        f"{skin_desc}, {realism_boost}, {lighting}, 8k UHD, masterpiece"
    )

    try:
        static_path = "static"
        if not os.path.exists(static_path):
            os.makedirs(static_path)

        # 3. 저장 차수(Group Number) 계산
        # 성별_차수_번호.png 구조를 위해 기존에 몇 번째 세트까지 생성됐는지 확인
        existing_groups = glob.glob(os.path.join(static_path, f"{data.gender}_*_1.png"))
        group_number = len(existing_groups) + 1

        image_urls = []

        # 4. 4장 연속 생성 루프
        for i in range(1, 5):
            # seed를 랜덤하게 부여하여 4장의 얼굴이 각각 다르게 나오도록 설정
            image = client.text_to_image(
                prompt=prompt,
                model=settings.FLUX_MODEL, 
                width=768, 
                height=1024,
                num_inference_steps=4,
                seed=random.randint(1, 1000000)
            )
            
            # 파일명 규칙: female_1_1.png, female_1_2.png ...
            filename = f"{data.gender}_{group_number}_{i}.png"
            save_path = os.path.join(static_path, filename)
            image.save(save_path)
            
            # 클라이언트에게 돌려줄 URL 리스트에 추가
            image_urls.append(f"/{save_path}")
        
        return {
            "status": "success", 
            "group_number": group_number,
            "image_urls": image_urls, 
            "prompt": prompt
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}