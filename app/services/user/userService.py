from uuid import uuid4
from app.models.userModel import User
from app.schemas.userSchemas import UserInfoRequest, ExternalIdealRequest, UserConcernRequest
from app.repositories.userRepo import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, req: UserInfoRequest) -> User:
        user = User(
            userId=str(uuid4()),
            userName=req.name,
            userGender=req.gender,
            userImage=req.image,
            userCustom=False,
            userConcern="",
            userIdealType=0
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
