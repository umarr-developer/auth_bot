from aiogram import Router
from src.handlers import globals, private

router = Router()
router.include_router(globals.router)
router.include_router(private.router)
