from fastapi import APIRouter, Response, Cookie, Depends, UploadFile, File, Form, BackgroundTasks
from app.schemas.userSchemas import UserConcernRequest
from typing import Optional, Literal
from app.dependency import getUserService, getImageGenService
from app.services.imageGen.imageGenService import ImageGenService
from app.services.user.userService import UserService
import logging

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
        samesite="none",
        max_age=60 * 60 * 24
    )

    return {
        "userId": user.userId
    }

@router.get(
    "/get",
    summary="정보 저장 테스트용"
)
def getUserInfo(userId: str, 
                service: UserService = Depends(getUserService)):
    return service.getUserIdService(userId)

from app.services.chat.concern_parser import parse_concern

@router.patch(
    "/concern",
    summary="사용자의 고민 입력",
    description="사용자에게 고민을 입력받고 저장함. 동시에 고민을 분석하여 장소를 추출함."
)
async def saveUserConcern(
    request: UserConcernRequest,
    userId: str,
    service: UserService = Depends(getUserService)
):
    # 1. 사용자 고민 저장
    updated_user = service.saveUserConcernService(userId, request)
    
    # 2. 고민 분석 (장소 추출)
    parsed_context = await parse_concern(request.concern)
    
    service.saveUserLocation(userId, parsed_context)
    return {
        "message": "고민 저장 및 장소 분석 완료",
        "parsed_context": parsed_context
    }

@router.patch(
    "/customIdeal",
    summary="사용자의 이상형 커스텀 여부 저장",
    description="사용자에게 이상형 커스텀 여부를 저장함."
)
def saveUserConcern(customIdeal: bool,
                    userId: str,
                    service: UserService = Depends(getUserService)):
    return service.chooseCustomIdealService(userId, customIdeal)

@router.patch(
    "/idealType",
    summary="사용자의 이상형 선택 저장",
    description="사용자가 선택한 이상형을 저장함."
)
def saveUserIdealType(idealType: int,
                    background_tasks: BackgroundTasks,
                    userId: str,
                    user_service: UserService = Depends(getUserService),
                    image_service: ImageGenService = Depends(getImageGenService),):
    # 1️⃣ 이상형 저장
    result = user_service.chooseIdealTypeService(userId, idealType)
    
    # 2️⃣ 이미지 생성은 백그라운드로
    background_tasks.add_task(
        generate_expression_bg,
        userId,
        image_service
    )
    return result

def generate_expression_bg(
    userId: str,
    image_service: ImageGenService
):
    image_service.generateExpressionService(userId)
    image_service.generateCoupleImageService(userId)

@router.patch(
    "/idealType",
    summary="사용자의 이상형 선택 저장",
    description="사용자가 선택한 이상형을 저장함."
)
def saveUserIdealType(idealType: int,
                    background_tasks: BackgroundTasks,
                    userId: str,
                    user_service: UserService = Depends(getUserService),
                    image_service: ImageGenService = Depends(getImageGenService),):
    # 1️⃣ 이상형 저장
    result = user_service.chooseIdealTypeService(userId, idealType)
    
    # 2️⃣ 이미지 생성은 백그라운드로
    background_tasks.add_task(
        generate_expression_bg,
        userId,
        image_service
    )
    return result

@router.get(
    "/checkImage",
    summary="이미지 생성을 체크함",
    description="사용자의 맞춤형 이상형이 생성되기를 기다림"
)
def checkImageGen(userId: str,
                    user_service: UserService = Depends(getUserService),):

    return user_service.checkImageGenService(userId)
