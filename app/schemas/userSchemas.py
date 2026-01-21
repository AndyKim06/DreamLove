from pydantic import BaseModel, Field
from typing import Optional, Literal
    
class UserConcernRequest(BaseModel):
    concern : str = Field(..., description = "사용자 고민")



