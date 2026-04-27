from fastapi import APIRouter
from app.api import passport_card

router = APIRouter()
router.include_router(passport_card.router)