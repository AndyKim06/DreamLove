from app.repositories.userMemoryRepo import UserMemoryRepository
from app.services.user.userService import UserService
from app.services.imageGen.imageGenService import ImageGenService
_repo = UserMemoryRepository()

def getUserService():
    return UserService(_repo)

def getImageGenService():
    return ImageGenService(_repo)

