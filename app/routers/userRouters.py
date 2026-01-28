from fastapi import APIRouter, Response, Cookie, Depends, UploadFile, File, Form, BackgroundTasks
from app.schemas.userSchemas import UserConcernRequest
from typing import Optional, Literal
from app.dependency import getUserService, getImageGenService
from app.services.imageGen.imageGenService import ImageGenService
from app.services.user.userService import UserService
router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post(
    "/info",
    summary="사용자의 정보 입력",
    description="사용자에게 정보를 입력받고 저장, 클라이언트에게 쿠키 or 세션줘서 식별가능하게함"
)
def saveUserInfo(
    response: Response,
    name: str = Form(...),
    gender: Literal["남자", "여자"] = Form(...),
    image: UploadFile = File(None),
    service: UserService = Depends(getUserService)
):
    user = service.create_user(name, gender, image)
    response.set_cookie(
        key="userId",
        value=user.userId,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24
    )

    return {
        "message": "사용자 정보 저장 완료",
        "userId": user.userId
    }

@router.get(
    "/get",
    summary="정보 저장 테스트용"
)
def getUserInfo(userId: str = Cookie(None), 
                service: UserService = Depends(getUserService)):
    return service.getUserIdService(userId)

@router.patch(
    "/concern",
    summary="사용자의 고민 입력",
    description="사용자에게 고민을 입력받고 저장함."
)
def saveUserConcern(request: UserConcernRequest,
                    userId: str = Cookie(None),
                    service: UserService = Depends(getUserService)):
    return service.saveUserConcernService(userId, request)

@router.patch(
    "/customIdeal",
    summary="사용자의 이상형 커스텀 여부 저장",
    description="사용자에게 이상형 커스텀 여부를 저장함."
)
def saveUserConcern(customIdeal: bool,
                    userId: str = Cookie(None),
                    service: UserService = Depends(getUserService)):
    return service.chooseCustomIdealService(userId, customIdeal)

@router.patch(
    "/idealType",
    summary="사용자의 이상형 선택 저장",
    description="사용자가 선택한 이상형을 저장함."
)
def saveUserIdealType(idealType: int,
                   # location: str,
                    background_tasks: BackgroundTasks,
                    userId: str = Cookie(None),
                    user_service: UserService = Depends(getUserService),
                    image_service: ImageGenService = Depends(getImageGenService),):
    # 1️⃣ 이상형 저장
    result = user_service.chooseIdealTypeService(userId, idealType)

    # # 2️⃣ 이미지 생성은 백그라운드로
    # background_tasks.add_task(
    #     generate_expression_bg,
    #     "park",
    #     userId,
    #     image_service
    # )

    return result

def generate_expression_bg(
    location: str,
    userId: str,
    image_service: ImageGenService
):
    image_service.generateExpressionService(location, userId)
