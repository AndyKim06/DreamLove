from fastapi import APIRouter
from app.schemas.idealSchemas import IdealRequest
from ..services.idealGen.idealService import generate_ideal_image_logic

router = APIRouter(prefix="/ideal", tags=["Ideal Type Generation"])

@router.post("/generate")
async def api_generate_ideal(request: IdealRequest):
    """
    사용자가 선택한 레퍼런스와 D.I.Y 속성을 기반으로 이상형 이미지를 생성합니다.
    """
    return await generate_ideal_image_logic(request)