from fastapi import FastAPI
from back.app.api.main import api_router
from back.app.api.services.llm import llm
import uvicorn
from contextlib import asynccontextmanager

app = FastAPI()
app.include_router(api_router)