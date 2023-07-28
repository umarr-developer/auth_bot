from aiogram import Router
from src.filters import PrivateTypeFilter
from src.handlers.private import admin, user

router = Router()
router.message.filter(PrivateTypeFilter())
router.include_router(admin.router)
router.include_router(user.router)
