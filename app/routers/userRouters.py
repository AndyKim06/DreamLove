from fastapi import APIRouter, Response, Cookie
from app.models.userSchemas import UserInfoRequest, ExternalIdealRequest, UserConcernRequest
from app.services.user.userService import saveUserInfoService, getUserIdService, saveUserConcernService
router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post(
    "/info",
    summary="사용자의 정보 입력",
    description="사용자에게 정보를 입력받고 저장, 클라이언트에게 쿠키 or 세션줘서 식별가능하게함"
)
async def saveUserInfo(request: UserInfoRequest, response: Response):
    userId = await saveUserInfoService(request)
    
    response.set_cookie(
        key="userId",
        value=userId,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24
    )

    return {
        "message": "사용자 정보 저장 완료",
        "userId": userId
    }

@router.get(
    "/get",
    summary="정보 저장 테스트용"
)
async def getUserInfo(userId: str = Cookie(None)):
    user = await getUserIdService(userId)
    return user

@router.post(
    "/concern",
    summary="사용자의 고민 입력",
    description="사용자에게 고민을 입력받고 저장함."
)
async def saveUserConcern(request: UserConcernRequest, userId: str = Cookie(None)):
    response = await saveUserConcernService(request, userId)
    return {
        "message": response,
    }
