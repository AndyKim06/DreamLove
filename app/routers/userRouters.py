from fastapi import APIRouter, HTTPException, status, Response, Cookie
from app.models.user.userSchemas import UserInfoRequest, ExternalIdealRequest, UserConcernRequest
from app.services.user.userService import saveUserInfo, getUserId, saveUserConcern
router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post(
    "/info",
    summary="사용자의 정보 입력",
    description="사용자에게 정보를 입력받고 저장, 클라이언트에게 쿠키 or 세션줘서 식별가능하게함"
)
async def saveUserInfoRequest(request: UserInfoRequest, response: Response):
    try:
        # 대화 흐름 실행
        userId = await saveUserInfo(request)
        
        response.set_cookie(
            key="userId",
            value=userId,
            httponly=True,
            secure=False,        # HTTPS면 True로 변경 권장
            samesite="lax",
            max_age=60 * 60 * 24
        )

        return {
            "message": "사용자 정보 저장 완료",
            "userId": userId
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"잘못된 요청: {str(e)}"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 오류: {str(e)}"
        )

@router.get(
    "/get",
    summary="정보 저장 테스트용"
)
async def getUserInfoRequest(userId: str = Cookie(None)):
    user = await getUserId(userId)
    return user

@router.post(
    "/concern",
    summary="사용자의 고민 입력",
    description="사용자에게 고민을 입력받고 저장함."
)
async def saveUserConcernRequest(request: UserConcernRequest, userId: str = Cookie(None)):
    # 대화 흐름 실행
    response = await saveUserConcern(request, userId)
    
    return {
        "message": response,
    }
