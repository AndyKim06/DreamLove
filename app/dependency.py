from app.repositories.userMemoryRepo import UserMemoryRepository
from app.services.user.userService import UserService

_repo = UserMemoryRepository()

def get_user_service():
    return UserService(_repo)
