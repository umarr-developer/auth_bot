from aiogram import Router
from src.handlers.globals import error

router = Router()
router.include_router(error.router)
