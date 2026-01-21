import os
from datetime import datetime
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# HF_TOKEN 가져오기
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN이 .env 파일에 설정되지 않았습니다!")

def generate_image(prompt, output_dir="outputs"):
    """
    FLUX.1-dev 모델을 사용하여 이미지 생성
    
    Args:
        prompt (str): 생성할 이미지의 프롬프트
        output_dir (str): 이미지를 저장할 디렉토리
        
    Returns:
        str: 저장된 이미지 파일 경로 (성공 시) 또는 None (실패 시)
    """
    try:
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # Inference Client 생성
        client = InferenceClient(token=HF_TOKEN)
        
        print("\n이미지 생성 중...")
        
        # 이미지 생성
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-dev"
        )
        
        # 파일명 생성 (프롬프트 기반)
        # 프롬프트를 파일명으로 사용 (특수문자 제거, 50자 제한)
        safe_prompt = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in prompt)
        safe_prompt = safe_prompt.replace(' ', '_')[:50]  # 공백을 _로, 50자 제한
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_prompt}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        # 이미지 저장
        image.save(filepath)
        
        return filepath
        
    except Exception as e:
        print(f"\n❌ 이미지 생성 실패: {e}")
        return None