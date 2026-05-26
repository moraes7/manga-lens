import shutil
import uuid
from fastapi import HTTPException
from pathlib import Path
from fastapi import UploadFile
from PIL import Image

UPLOAD_FOLDER = Path("app/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

def save_image(file: UploadFile):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail="Formato de imagem inválido. Apenas PNG, JPG e JPEG são aceitos."
        )
    
    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_FOLDER / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return unique_filename

def get_image_info(image_path):
    image = Image.open(image_path)

    return {
        "format": image.format,
        "size": image.size,
        "mode": image.mode
    }

def preprocess_image(image_path):
    image = Image.open(image_path)

    image = image.convert("RGB")
    
    image = image.resize((224, 224))

    processed_filename = f"processed_{Path(image_path).name}"
    processed_path = UPLOAD_FOLDER / processed_filename

    image.save(processed_path)

    return {
        "processed_filename": processed_filename,
        "size": image.size,
        "mode": image.mode
    }