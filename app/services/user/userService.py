import uuid
from app.models.user.userSchemas import UserInfoRequest, ExternalIdealRequest

fake_user_db = {}

async def userInfoService(request: UserInfoRequest):
    user_id = str(uuid.uuid4())

    fake_user_db[user_id] = {
        "name": request.name,
        "gender": request.gender,
        "image": request.image
    }

    return user_id

async def get_user_id(name: str) -> str:
    for user_id, user in fake_user_db.items():
        if user["name"] == name:
            return user_id

    raise ValueError("해당 이름의 사용자가 존재하지 않습니다.")