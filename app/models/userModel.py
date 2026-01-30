from pydantic import BaseModel
from typing import Optional, Literal

class User(BaseModel):
    userId: str # pk
    userName: str
    userGender: Literal["남자", "여자"]
    userImage: Optional[str] = None
    userConcern: Optional[str] = None
    userCustom : bool
    userIdealType : int
    userLocation : str
