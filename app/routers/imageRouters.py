from fastapi import APIRouter, Response, Cookie, Depends
from fastapi.responses import FileResponse
from app.services.imageGen.imageGenService import ImageGenService
from app.dependency import getImageGenService
from app.schemas.imageGenSchemas import ExternalIdealRequest
import qrcode
import tempfile

router = APIRouter(
    prefix="/imageGen",
    tags=["imageGen"]
)

@router.post(
    "/idealImage",
    summary="사용자가 선택한 요소를 가지고 이상형을 생성함",
)
def generateIdeal( request : ExternalIdealRequest,
                     userId: str,
                     service: ImageGenService = Depends(getImageGenService),
                    ):
    image_paths = service.generateIdealImageService(request=request, userId=userId)
    return {
        "images": image_paths
    }

@router.post(
    "/idealExpressChange",
    summary="사용자가 선택한 이상형의 표정 변환 사진을 생성함",
)
def changeExpression(location: str,
                     userId: str,
                     service: ImageGenService = Depends(getImageGenService)
                    ):
    image = service.generateExpressionService(location, userId)
    return "ok"

@router.post(
    "/resultImage",
    summary="성공시 이상형과의 셀카사진을 생성함",
)
def generateCoupleImage(location: str,
                     userId: str,
                     service: ImageGenService = Depends(getImageGenService)
                    ):
    image_path = service.generateCoupleImageService(location, userId)
    return FileResponse(
            path=image_path,
            media_type="image/png",
            filename="couple.png"
        )

@router.get("/idealList", summary="이상형 리스트 반환")
def download_test_image(userId: str,
                        service: ImageGenService = Depends(getImageGenService)):
    image_paths = service.getIdealImageList(userId)
    return {
        "images": image_paths
    }

@router.get("/download", summary="test.png 다운로드")
def download_test_image():
    return FileResponse(
        path="C:\\Users\\Gamzadole\\Desktop\\DreamLove\\app\\imageCloud\\test.png",
        media_type="image/png",
        filename="test.png"
    )


@router.get("/download/qr", summary="test.png 다운로드용 QR 코드")
def get_test_image_qr():
    download_url = "http://localhost:8000/imageGen/download"

    qr = qrcode.make(download_url)

    # 임시 파일로 QR 생성
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    qr.save(tmp_file.name)

    return FileResponse(
        path=tmp_file.name,
        media_type="image/png",
        filename="test_image_qr.png"
    )