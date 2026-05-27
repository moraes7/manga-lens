from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
from app.services.image_service import (
    save_image, 
    get_image_info, 
    preprocess_image,
    generate_embedding,
    find_similar_image
    )
from app.integrations.trace_moe import (
    search_anime_by_image,
    ERROR_STATUS_MAP
)

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = save_image(file)

    image_path = Path("app/uploads") / filename

    image_info = get_image_info(image_path)

    processed_image = preprocess_image(image_path)

    embedding = generate_embedding(image_path)

    similar_image = find_similar_image(image_path)

    trace_moe_result = search_anime_by_image(image_path)

    if not trace_moe_result["success"]:
        error_code = trace_moe_result.get("error_code")

        status_code = ERROR_STATUS_MAP.get(error_code, 500)

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": trace_moe_result["message"],
                "filename": filename,
                "image_info": image_info,
                "preprocessed_image": processed_image,
                "embedding_preview": embedding[:10],
                "similar_image": similar_image,
                "trace_moe_result": trace_moe_result
            }
        )
    
    return {
        "success": True,
        "message": "Imagem processada com sucesso",
        "filename": filename,
        "image_info": image_info,
        "preprocessed_image": processed_image,
        "embedding_preview": embedding[:10],
        "similar_image": similar_image,
        "trace_moe_result": trace_moe_result
    }