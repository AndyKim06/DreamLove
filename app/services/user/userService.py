from uuid import uuid4
from fastapi import UploadFile
from app.models.userModel import User
from app.schemas.userSchemas import UserConcernRequest
from app.repositories.userRepo import UserRepository
from PIL import Image
import os
from pathlib import Path
from deep_translator import GoogleTranslator

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, name:str, gender:str, image: UploadFile) -> User:
        userId = str(uuid4())
        
        # 상대 경로 사용 및 디렉토리 자동 생성
        image_dir = Path("frontend/imageCloud/user")
        image_dir.mkdir(parents=True, exist_ok=True)
        
        image_path = str(image_dir / f"{userId}.png")
        with open(image_path, "wb") as f:
            f.write(image.file.read())

        user = User(
            userId= userId,
            userName=name,
            userGender=gender,
            userImage=image_path,
            userCustom=False,
            userConcern="",
            userIdealType=0,
            userLocation=""
        )
        return self.repo.save(user)

    def getUserIdService(self, userId: str) -> User:
        user = self.repo.findById(userId)
        if not user:
            raise ValueError("User not found")
        return user

    def saveUserConcernService(self, userId: str, request: UserConcernRequest):
        user = self.repo.findById(userId)
        if not user:
            raise ValueError("User not found")

        user.userConcern = request.concern
        return self.repo.save(user)

    def saveUserLocation(self, userId: str, parsed_context: any):
        user = self.repo.findById(userId)
        if not user:
            raise ValueError("User not found")

        korean_location = parsed_context.location

        try:
            translated_location = GoogleTranslator(source='ko', target='en').translate(korean_location)
            user.userLocation = translated_location
        except Exception as e:
            user.userLocation = korean_location 

        return self.repo.save(user)
    
    def chooseCustomIdealService(self, userId: str, customIdeal: bool):
        user = self.repo.findById(userId)
        if not user:
            raise ValueError("User not found")

        user.userCustom = customIdeal
        return self.repo.save(user)

    def chooseIdealTypeService(self, userId: str, idealType: int):
        user = self.repo.findById(userId)
        if not user:
            raise ValueError("User not found")

        user.userIdealType = idealType
        return self.repo.save(user)
