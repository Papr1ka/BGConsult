from fastapi import APIRouter

from back.app.api.routes import question, rag

api_router = APIRouter()
api_router.include_router(question.router)
# api_router.include_router(rag.router)
