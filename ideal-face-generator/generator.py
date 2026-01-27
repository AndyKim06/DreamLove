# generator.py - FLUX API 이미지 생성 로직 (4장 생성)

import os
from datetime import datetime
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN이 .env 파일에 설정되지 않았습니다!")

def generate_image(prompt_eng, negative_prompt, prompt_kor, output_dir="output", num_images=4):
    """
    FLUX.1-dev 모델로 이미지 여러 장 생성
    
    Args:
        prompt_eng: 영문 프롬프트
        negative_prompt: 네거티브 프롬프트
        prompt_kor: 한글 요약 (파일명용)
        output_dir: 저장 디렉토리
        num_images: 생성할 이미지 개수 (기본 4장)
    
    Returns:
        생성된 이미지 파일 경로 리스트 또는 None
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        client = InferenceClient(token=HF_TOKEN)
        
        print(f"\n{'='*60}")
        print(f"이미지 {num_images}장 생성 시작")
        print(f"프롬프트: {prompt_kor}")
        print(f"{'='*60}\n")
        
        generated_files = []
        
        for i in range(num_images):
            print(f"[{i+1}/{num_images}] 생성 중...", end=" ", flush=True)
            
            try:
                image = client.text_to_image(
                    prompt=prompt_eng,
                    model="black-forest-labs/FLUX.1-dev",
                    negative_prompt=negative_prompt,
                    guidance_scale=7.5,
                    num_inference_steps=50,
                    height=1024,
                    width=1024
                )
                
                # 파일명 생성
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_kor = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in prompt_kor)
                safe_kor = safe_kor.replace(' ', '_')[:50]
                filename = f"{timestamp}_{safe_kor}_{i+1}.png"
                filepath = os.path.join(output_dir, filename)
                
                # 저장
                image.save(filepath)
                generated_files.append(filepath)
                
                print(f"완료!")
                
            except Exception as e:
                print(f"실패: {e}")
                continue
        
        print(f"\n{'='*60}")
        print(f"총 {len(generated_files)}/{num_images}장 생성 완료")
        print(f"{'='*60}\n")
        
        if generated_files:
            print("생성된 파일:")
            for idx, file in enumerate(generated_files, 1):
                print(f"  [{idx}] {file}")
            print()
        
        return generated_files if generated_files else None
        
    except Exception as e:
        print(f"전체 생성 실패: {e}")
        return None