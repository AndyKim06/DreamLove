# API 테스트

from generator import generate_image

prompt_eng = "A beautiful 20-year-old Korean woman, photorealistic portrait, studio lighting"
prompt_kor = "20대 한국 여성 테스트"

result = generate_image(prompt_eng, prompt_kor)

if result:
    print(f"\n테스트 성공!")
else:
    print(f"\n테스트 실패")