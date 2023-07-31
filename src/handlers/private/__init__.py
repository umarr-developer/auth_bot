from aiogram import Router
from src.filters import PrivateTypeFilter
from src.handlers.private import user

router = Router()
router.message.filter(PrivateTypeFilter())
router.include_router(user.router)
