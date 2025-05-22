from pathlib import Path

import uvicorn
from fastapi import FastAPI
from back.app.api.main import api_router
from back.app.core.storage.postgres import Base, engine

app = FastAPI()
app.include_router(api_router)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8080)