from pydantic import BaseModel, Field
from typing import Optional, Literal

class UserInfoRequest(BaseModel):
    name: str = Field(..., description="사용자 이름")
    gender: Literal["남자", "여자"] = Field(..., description="성별")
    image: Optional[str] = Field(None, description="프로필 이미지")
    
class UserConcernRequest(BaseModel):
    concern : str = Field(..., description = "사용자 고민")



