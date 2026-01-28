from pydantic import BaseModel, Field
from typing import Literal

class IdealRequest(BaseModel):
    gender: Literal["male", "female"] = Field(..., description="이상형 성별")
    ref_type: Literal["Type 1", "Type 2", "Type 3", "Type 4"] = Field(..., description="동물상 레퍼런스")
    hair: str = Field(..., description="헤어스타일")
    eyelid: str = Field(..., description="쌍꺼풀 유무")
    mood: str = Field(..., description="전체적인 분위기")
    makeup: str = Field(..., description="메이크업 강도")
    outfit: str = Field(..., description="의상")
    face_shape: str = Field(..., description="얼굴형")
    skin_tone: int = Field(..., ge=0, le=100, description="피부톤 슬라이더 (0-100)")