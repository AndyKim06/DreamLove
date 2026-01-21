from abc import ABC, abstractmethod
from models.userModel import User

class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def findById(self, user_id: str) -> User | None:
        pass
