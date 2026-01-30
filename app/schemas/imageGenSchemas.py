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

class ExternalIdealRequest(BaseModel):
    animal_type : str
    eyelid : str
    faceShape : str
    hair : str
    clothe : str
    makeup : str
    skin : int
