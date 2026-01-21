from typing import Dict
from app.models.userModel import User
from app.repositories.userRepo import UserRepository

class UserMemoryRepository(UserRepository):
    def __init__(self):
        self._store: Dict[str, User] = {}

    def save(self, user: User) -> User:
        self._store[user.userId] = user
        return user

    def findById(self, user_id: str) -> User | None:
        return self._store.get(user_id)
