from aiogram import Router

from src.filters.chat import UserFilter
from src.handlers.private.user import about, file_id, start, test
from src.middlewares import ThrottlingMiddleware

router = Router()
router.message.middleware(ThrottlingMiddleware())
router.include_router(start.router)
router.include_router(file_id.router)
router.include_router(test.router)
router.include_router(about.router)
