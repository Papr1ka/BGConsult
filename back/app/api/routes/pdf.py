from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import shutil
import os

from back.app.core.config import games_info_by_file, games_info_by_name
from back.app.core.storage.qdrant import qdrant
from back.app.models.pdf import Game
from back.app.core.paths import BASE_DIR

router = APIRouter()

GAMES_DIR = BASE_DIR / "games"

# Создаем папку, если не существует
os.makedirs(GAMES_DIR, exist_ok=True)

@router.post("/upload_pdf/")
async def upload_pdf(
    name: str = Form(...),
    url: str = Form(...),
    file: UploadFile = File(...)
):
    # Проверка расширения
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_location = os.path.join(GAMES_DIR, file.filename)

    try:
        # Сохраняем файл
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    games_info_by_name[name] = Game(name=name, url=url, file_name=file.filename)
    games_info_by_file[file.filename] = Game(name=name, url=url, file_name=file.filename)

    print("ff", file_location, file.filename)
    qdrant.create_qdrant_collection(file.filename)
    qdrant.upload_to_qdrant(file.filename)


    return {
        "message": "Файл успешно загружен",
        "name": name,
        "url": url,
        "filename": file.filename
    }


@router.delete("/delete_pdf/{filename}")
async def delete_pdf(filename: str):
    file_path = os.path.join(GAMES_DIR, games_info_by_name.get(filename).file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    return {"detail": f"File '{filename}' deleted successfully"}


@router.get("/list_games")
async def list_games():
    """
    Возвращает список названий игр (не имена файлов), доступных в папке pdf_games.
    """
    games = []
    for file in GAMES_DIR.glob("*.pdf"):
        game_name = games_info_by_file.get(file.name)
        if game_name:
            games.append(game_name.name)
    return games