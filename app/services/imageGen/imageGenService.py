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
from huggingface_hub import InferenceClient
from promptBuilder import PromptBuilder
import logging
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

        load_dotenv()
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.HF_TOKEN = os.getenv("HF_TOKEN")

        self.geminiClient = genai.Client(self.GEMINI_API_KEY)
        self.hfClient = InferenceClient(token=self.HF_TOKEN)
        self.promptBuilder = PromptBuilder()
        self.aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")  
    
    def generateIdealImageService(self, request :ExternalIdealRequest, userId:str):
        user = self.repo.findById(userId)
        ideal_gender = "female" if user.userGender == "남자" else "male"
        ideal_animal = request.animal_type
        ideal_eyelid = request.eyelid
        ideal_faceShape = request.faceShape
        ideal_hair= request.hair
        ideal_clothe = request.clothe
        ideal_makeup = request.makeup
        ideal_skinTone = request.skin

        prompt_eng, negative_prompt, tokens = self.promptBuilder.build_prompt(gender=ideal_gender, animal=ideal_animal, eyelid=ideal_eyelid, face_shape=ideal_faceShape,
                                        hairstyle=ideal_hair, clothing=ideal_clothe, makeup=ideal_makeup, skintone=ideal_skinTone)
        

        logging.info(f"Prompt token = {tokens}, Image Generating")
        logging.info(f"gender = {ideal_gender}, ideal_animal = {ideal_animal}, ideal_eyelid = {ideal_eyelid}, ideal_faceShape = {ideal_faceShape}")
        logging.info(f"ideal hair = {ideal_hair}, ideal_clothe = {ideal_clothe}, ideal_makeup = {ideal_makeup}, ideal_skinTone = {ideal_skinTone}")

        for i in range(4):
            image_path = ""
            image = self.hfClient.text_to_image(
                    prompt=prompt_eng,
                    model="black-forest-labs/FLUX.1-dev",
                    negative_prompt=negative_prompt,
                    guidance_scale=7.5,
                    num_inference_steps=50,
                    height=1024,
                    width=1024
                )
            image.save(image_path)
            logging.info(f"{i+1}번째 사진 생성 완료")
        return 
    
    def getUserIdealImagePath(self, userId):
        user = self.repo.findById(userId)
        if user.userCustom:
            idealImage = f"C:\\Users\\Gamzadole\\Desktop\\DreamLove\\app\\imageCloud\\{userId}__{user.userIdealType}.png"
        else:
            if user.userGender == "남자":
                idealImage = f"C:\\Users\\Gamzadole\\Desktop\\DreamLove\\app\\imageCloud\\standard_female_{user.userIdealType}.png"
            else:
                idealImage = f"C:\\Users\\Gamzadole\\Desktop\\DreamLove\\app\\imageCloud\\standard_male_{user.userIdealType}.png"
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
                response = self.geminiClient.models.generate_content(
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
            response = self.geminiClient.models.generate_content(
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
                        file_name = f"C:\\Users\\Gamzadole\\Desktop\\DreamLove\\app\\imageCloud\\{user.userId}_success_result"
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
