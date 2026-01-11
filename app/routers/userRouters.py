from fastapi import APIRouter, HTTPException, status, Response
from app.models.user.userSchemas import UserInfoRequest, ExternalIdealRequest
from app.services.user.userService import userInfoService, get_user_id
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
    try:
        # 대화 흐름 실행
        user_id = await userInfoService(request)
        
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            secure=False,        # HTTPS면 True로 변경 권장
            samesite="lax",
            max_age=60 * 60 * 24
        )

        return {
            "message": "사용자 정보 저장 완료",
            "user_id": user_id
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
async def getUserInfo(name: str):
    user_id = await get_user_id(name)
    return user_id