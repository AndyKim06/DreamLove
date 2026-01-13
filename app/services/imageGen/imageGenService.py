from google import genai
from PIL import Image
from io import BytesIO
import time
from dotenv import load_dotenv
import os
from aura_sr import AuraSR

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(GEMINI_API_KEY)
aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")

ROLE_INSTRUCTION = """
You are a professional image generation model specialized in preserving human identity.

You MUST strictly follow these rules:
1. The provided person image defines the identity.
   The face, facial structure, age, and all identity-related features must be preserved exactly.
2. The location described in the prompt defines the background.
   All generated images must use the SAME location and environment.
3. The background, clothing, hairstyle, lighting, and camera angle must remain identical across all images.
4. The person MUST face directly forward, looking straight at the camera.
   No side view, no angled face, no looking away.
5. Only the facial expression is allowed to change.
6. Generate images of the same person.

Negative Prompt:
face change, identity change, different person, face swap,
background inconsistency, different location,
clothing change, hairstyle change,
cartoon, anime, illustration,
low quality, blurry, distorted face, exaggerated emotion
"""

def generateExpressionService(location, image):
    expressions = ["Smiling", "Neutral", "Disappointed"]
    for i, exp_name in enumerate(expressions):
        print(f"이미지 생성 중 ({i+1}/3): {exp_name} expression...")
        
        current_prompt = f"""
        Using the provided reference image of a person, place the SAME person naturally in the following location:

        Location: {location}

        Generate a photorealistic image of the same person in the SAME location.
        The person must wear the same clothing and have the same hairstyle as in the reference.
        The background, lighting, and composition must remain consistent.

        The facial expression should be: {exp_name}
        
        Do NOT exaggerate facial expressions.
        Do NOT change identity, clothing, or background.
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[current_prompt, image],
                config={
                    "system_instruction": ROLE_INSTRUCTION,
                    "temperature": 0.7
                }
            )

            if response.candidates:
                candidate = response.candidates[0]
                for part in candidate.content.parts:
                    if part.inline_data is not None:
                        img_data = Image.open(BytesIO(part.inline_data.data))
                        file_name = f"generated_expression_{exp_name}.png"
                        img_data.save(file_name)
                        print(f"Saved: {file_name}")
                    elif part.text is not None:
                        print(f"Model text: {part.text}")

            time.sleep(1)

        except Exception as e:
            print(f"Error during {exp_name} generation: {e}")


def generateCoupleImageService(location, image1, image2):
    current_prompt = f"""
    Using the provided TWO reference images of two different people, place the SAME two people together naturally in the following location:

    Location: {location}

    Generate a photorealistic image of the SAME two people taking a selfie together in the SAME location.

    Both people must:
    - Preserve their exact identities as shown in their respective reference images
    - Have the same facial structure, age, and personal features
    - Wear the same clothing and have the same hairstyles as in the reference images

    The image should:
    - Be framed as a natural selfie photo taken by one of the two people
    - Show both people clearly within the frame
    - Use a realistic selfie composition (arm slightly extended, close camera distance, casual framing)
    - Maintain consistent background, lighting, and environment based on the location

    Do NOT exaggerate facial expressions.
    Do NOT change identities, clothing, hairstyles, or background.
    Do NOT introduce additional people.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[current_prompt, image1, image2],
            config={
                "system_instruction": ROLE_INSTRUCTION,
                "temperature": 0.7
            }
        )

        if response.candidates:
            candidate = response.candidates[0]
            for part in candidate.content.parts:
                if part.inline_data is not None:
                    img_data = Image.open(BytesIO(part.inline_data.data))
                    file_name = f"generated_result.png"
                    img_data.save(file_name)
                    print(f"Saved: {file_name}")
                elif part.text is not None:
                    print(f"Model text: {part.text}")

        time.sleep(1)

    except Exception as e:
        print(f"Error during generation: {e}")


def upscalingImageService(image):
    img = image.convert("RGB") 
    out = aura_sr.upscale_4x_overlapped(img)
    out.save("upsacled_image2.png")
