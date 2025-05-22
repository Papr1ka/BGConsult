from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from back.app.core.paths import BASE_DIR

router = APIRouter()

UPLOAD_DIR = BASE_DIR / "games"

# Создаем папку, если не существует
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Проверяем расширение файла
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Сохраняем файл
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()



    return {"filename": file.filename, "saved_to": file_location}


@router.delete("/delete_pdf/{filename}")
async def delete_pdf(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    return {"detail": f"File '{filename}' deleted successfully"}
