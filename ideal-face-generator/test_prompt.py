# 프롬프트 조합 테스트

from prompts import build_prompt

# 테스트 파라미터
prompt_eng, prompt_kor, tokens = build_prompt(
    gender="female",
    animal="cat",
    eyelid="double",
    face_shape="v-line",
    hairstyle="long",
    clothing="shirt",
    makeup="light",
    skintone_value=35
)

print(f"영문 프롬프트:\n{prompt_eng}\n")
print(f"한글 프롬프트:\n{prompt_kor}\n")
print(f"토큰 수: {tokens}/77")