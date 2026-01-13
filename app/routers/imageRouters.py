from fastapi import APIRouter, Response, Cookie
from app.services.imageGen.imageGenService import generateExpressionService, generateCoupleImageService

router = APIRouter(
    prefix="/imageGen",
    tags=["imageGen"]
)

# 좀 연결되고 진행해야할 거 같음