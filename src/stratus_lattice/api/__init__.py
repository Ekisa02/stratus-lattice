from fastapi import APIRouter
from . import handlers

router = APIRouter()
router.include_router(handlers.router)
