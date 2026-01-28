from google import genai
from PIL import Image
from io import BytesIO
import time
from dotenv import load_dotenv
import os
from aura_sr import AuraSR
from app.models.userModel import User
from app.repositories.userRepo import UserRepository
from app.schemas.imageGenSchemas import ExternalIdealRequest

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

class ImageGenService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

        load_dotenv("gemini_api_key.env")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(self.GEMINI_API_KEY)
        self.aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")
    
    def generateIdealImageService(self, request :ExternalIdealRequest):
        return 
    
    def getUserIdealImagePath(self, userId):
        user = self.repo.findById(userId)
        base_path = os.getcwd()
        image_cloud_path = os.path.join(base_path, "app", "imageCloud")
        
        if user.userCustom:
            idealImage = os.path.join(image_cloud_path, f"{userId}__{user.userIdealType}.png")
        else:
            if user.userGender == "남자":
                idealImage = os.path.join(image_cloud_path, f"standard_female_{user.userIdealType}.png")
            else:
                idealImage = os.path.join(image_cloud_path, f"standard_male_{user.userIdealType}.png")
        return idealImage
    
    def generateExpressionService(self, location:str, userId:str):
        image_path = self.getUserIdealImagePath(userId)
        image = Image.open(image_path)

        expressions = ["Smiling", "Neutral", "Disappointed"]
        for i, exp_name in enumerate(expressions):
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
                response = self.client.models.generate_content(
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
                            file_name = f"{image_path}_{exp_name}.jpg"
                            img_data.save(file_name)
                            print(f"Saved: {file_name}")
                        elif part.text is not None:
                            print(f"Model text: {part.text}")

                time.sleep(1)

            except Exception as e:
                print(f"Error during {exp_name} generation: {e}")


    def generateCoupleImageService(self, location, userId):
        user = self.repo.findById(userId)
        idealImage = self.getUserIdealImagePath(userId)
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
            response = self.client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[current_prompt, user.userImage, idealImage],
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
                        base_path = os.getcwd()
                        file_name = os.path.join(base_path, "app", "imageCloud", f"{user.userId}_success_result.png")
                        img_data.save(file_name)
                        print(f"Saved: {file_name}")
                    elif part.text is not None:
                        print(f"Model text: {part.text}")
        except Exception as e:
            print(f"Error during generation: {e}")


    def upScalingImage(self, image, userId):
        image_path = self.getUserIdealImagePath(userId)
        image = open(image_path).convert("RGB")
        out = self.aura_sr.upscale_4x_overlapped(image)
        out.save(image_path)
