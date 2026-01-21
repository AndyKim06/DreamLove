from repositories.userMemoryRepo import UserMemoryRepository
from services.user.userService import UserService

_repo = UserMemoryRepository()

def get_user_service():
    return UserService(_repo)
