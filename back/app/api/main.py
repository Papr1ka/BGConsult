from fastapi import APIRouter

from back.app.api.routes import question

api_router = APIRouter()
api_router.include_router(question.router)
