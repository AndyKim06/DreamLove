import uuid
from models.userModel import User
from app.schemas.userSchemas import UserInfoRequest, ExternalIdealRequest, UserConcernRequest
from repositories.userRepo import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, req: UserInfoRequest) -> User:
        user = User(
            userId=str(uuid()),
            name=req.name,
            gender=req.gender,
            image=req.image
        )
        return self.repo.save(user)

    def getUserIdService(self, userId: str) -> User:
        user = self.repo.find_by_id(userId)
        if not user:
            raise ValueError("User not found")
        return user

    def saveUserConcernService(self, request: UserConcernRequest, userId: str):
        user = self.repo.findById(userId)
        if not user:
            raise ValueError("User not found")

        user.concern = request.concern
        return self.repo.save(user)



