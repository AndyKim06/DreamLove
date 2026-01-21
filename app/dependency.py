from app.repositories.userMemoryRepo import UserMemoryRepository
from app.services.user.userService import UserService

_repo = UserMemoryRepository()

def getUserService():
    return UserService(_repo)

