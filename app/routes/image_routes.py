from fastapi import APIRouter, File, UploadFile
from pathlib import Path
from app.services.image_service import (save_image, get_image_info, preprocess_image)

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = save_image(file)

    image_path = Path("app/uploads") / filename

    image_info = get_image_info(image_path)

    precessed_image = preprocess_image(image_path)
    
    return {
        "filename": filename,
        "message": "Imagem enviada com sucesso!", 
        "image_info": image_info,
        "preprocessed_image": precessed_image
    }