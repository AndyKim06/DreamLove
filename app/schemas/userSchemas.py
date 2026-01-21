# usermodel.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum

class FaceShape(str, Enum):
    EGG = "계란형"
    ROUND = "둥근형"
    ANGULAR = "각진형"


class Eyes(str, Enum):
    BIG = "큰눈"
    SLIM_LONG = "가늘고긴눈"


class Eyelid(str, Enum):
    NONE = "무쌍"
    INNER = "속쌍"
    OUTER = "겉쌍"


class Hair(str, Enum):
    LONG_STRAIGHT = "장발생머리"
    LONG_WAVE = "장발웨이브"
    LONG_CURLY = "장발곱슬"
    SHORT_STRAIGHT = "단발생머리"
    SHORT_WAVE = "단발웨이브"
    SHORT_CUT = "숏컷"


class UserInfoRequest(BaseModel):
    name: str = Field(..., description="사용자 이름")
    gender: Literal["남자", "여자"] = Field(..., description="성별")
    image: Optional[str] = Field(None, description="프로필 이미지")
    
class UserConcernRequest(BaseModel):
    concern : str = Field(..., description = "사용자 고민")
    
class ExternalIdealRequest(BaseModel):
    reference: int = Field(..., description="외적 이상형 레퍼런스")
    faceShape: FaceShape = Field(..., description="얼굴형")
    eyes: Eyes = Field(..., description="눈 형태")
    eyelid: Eyelid = Field(..., description="쌍꺼풀 유형")
    hair: Hair = Field(..., description="헤어 스타일")
    bangs: bool = Field(..., description="앞머리 유무")


