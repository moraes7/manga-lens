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
from app.schemas.image_schema import UploadImageResponse
from app.services.anime_detector_service import detect_anime

router = APIRouter()

@router.post(
        "/upload",
        #response_model=UploadImageResponse,
        summary="Upload de imagem para análise",
        description="Recebe uma imagem, processa o arquivo, gera embedding, busca imagens similares e consulta a API trace.moe para identificar o anime.",
        responses={
            200: {
                "description": "Imagem processada com sucesso"
            },
            400: {
                "description": "Nenhum resultado encontrado"
            },
            422: {
                "description": "Resultado encontrado com baixa confiança"
            },
            502: {
                "description": "Erro ao consultar a API do trace.moe"
            },
            504: {
                "description": "Timeout ao consultar a API do trace.moe"
            },
            500: {
                "description": "Erro interno inesperado"
            }
        }   
    )

async def upload_image(file: UploadFile = File(...)):
    filename = save_image(file)

    image_path = Path("app/uploads") / filename

    image_info = get_image_info(image_path)

    processed_image = preprocess_image(image_path)

    embedding = generate_embedding(image_path)

    similar_image = find_similar_image(image_path)

    trace_moe_result = detect_anime(image_path)

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
                "anime_result": trace_moe_result
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
        "anime_result": trace_moe_result
    }