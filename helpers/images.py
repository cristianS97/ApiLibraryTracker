import os
import uuid
import shutil
from pathlib import Path
from fastapi import HTTPException, UploadFile

UPLOAD_DIR = Path("static/books")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_book_image(file: UploadFile, title: str, author: str) -> str:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG o PNG")

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}_{title}_{author}.{file_extension}".replace(" ", "_")
    file_path = UPLOAD_DIR / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/static/books/{unique_filename}"

def delete_book_image(image_url: str):
    if image_url:
        relative_path = image_url.lstrip("/")
        full_path = Path(relative_path)
        if full_path.exists():
            os.remove(full_path)