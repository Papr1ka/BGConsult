from fastapi import APIRouter

from back.app.api.routes import question, pdf

api_router = APIRouter()
api_router.include_router(question.router)
api_router.include_router(pdf.router)
