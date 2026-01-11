import uuid
from app.models.user.userSchemas import UserInfoRequest, ExternalIdealRequest, UserConcernRequest

fake_user_db = {}

async def saveUserInfoService(request: UserInfoRequest):
    user_id = str(uuid.uuid4())

    fake_user_db[user_id] = {
        "name": request.name,
        "gender": request.gender,
        "image": request.image
    }

    return user_id

async def getUserIdService(userId: str):
    return fake_user_db.get(userId)

async def saveUserConcernService(request: UserConcernRequest, userId: str):
    fake_user_db[userId]["concern"] = request.concern
    return "ok"

