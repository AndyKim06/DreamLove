from fastapi import APIRouter, Response, Cookie, Depends
from app.services.imageGen.imageGenService import ImageGenService
from app.dependency import getImageGenService
router = APIRouter(
    prefix="/imageGen",
    tags=["imageGen"]
)

@router.post(
    "/idealExpressChange",
    summary="사용자가 선택한 이상형의 표정 변환 사진을 생성함",
)
def changeExpression(location: str,
                     userId: str = Cookie(None),
                     service: ImageGenService = Depends(getImageGenService)
                    ):
    image = service.generateExpressionService(location, userId)
    return "ok"

@router.post(
    "/resultImage",
    summary="성공시 이상형과의 셀카사진을 생성함",
)
def changeExpression(location: str,
                     userId: str = Cookie(None),
                     service: ImageGenService = Depends(getImageGenService)
                    ):
    image = service.generateCoupleImageService(location, userId)
    return "ok"
    