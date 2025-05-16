from fastapi import FastAPI
from back.app.api.main import api_router
import uvicorn
from contextlib import asynccontextmanager

app = FastAPI()
@app.on_event("startup")
async def show_routes():
    print("Registered routes:")
    for route in app.routes:
        print(f"{route.path} → {route.name} [{route.methods}]")

app.include_router(api_router)