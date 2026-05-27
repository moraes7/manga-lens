# CÓDIGO NOVO
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TraceMoeData(BaseModel):
    anime: str = Field(example="NOME DO ANIME")
    episode: Optional[int] = Field(default=None, example=112)
    similarity: float = Field(example=92.51)
    timestamp: str = Field(example="19:31")
    preview: Optional[str] = Field(
        default=None,
        example="https://api.trace.moe/image/example"
    )


class TraceMoeResult(BaseModel):
    success: bool = Field(example=True)
    data: Optional[TraceMoeData] = None
    error_code: Optional[str] = Field(default=None, example=None)
    message: Optional[str] = Field(default=None, example=None)


class UploadImageResponse(BaseModel):
    success: bool = Field(example=True)
    message: str = Field(example="Imagem processada com sucesso")
    filename: str = Field(example="anime_image.png")
    image_info: Dict[str, Any] = Field(
        example={
            "format": "PNG",
            "size": [1280, 720],
            "mode": "RGB"
        }
    )
    preprocessed_image: Dict[str, Any] = Field(
        example={
            "status": "Imagem pré-processada com sucesso",
            "size": [224, 224]
        }
    )
    embedding_preview: List[float] = Field(
        example=[0.12, 0.45, 0.78, 0.33]
    )
    similar_image: Any = Field(
        example={
            "filename": "reference_image.png",
            "similarity": 0.91
        }
    )
    trace_moe_result: TraceMoeResult