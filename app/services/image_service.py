import shutil
import uuid
from fastapi import HTTPException
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
import torch
from torchvision import models, transforms

UPLOAD_FOLDER = Path("app/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

REFERENCE_FOLDER = Path("app/reference_images")

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

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
    
    image.thumbnail((512, 512))

    processed_filename = f"processed_{Path(image_path).name}"
    processed_path = UPLOAD_FOLDER / processed_filename

    image.save(processed_path, quality=95)

    return {
        "processed_filename": processed_filename,
        "size": image.size,
        "mode": image.mode
    }

def generate_embedding(image_path):
    image = Image.open(image_path).convert("RGB")

    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        embedding = model(image_tensor)
    
    embedding = embedding.flatten().tolist()

    return embedding

def compare_embeddings(embedding_a, embedding_b):
    vector_a = torch.tensor(embedding_a)
    vector_b = torch.tensor(embedding_b)

    similarity = torch.nn.functional.cosine_similarity(
        vector_a.unsqueeze(0), 
        vector_b.unsqueeze(0)
    )

    return similarity.item()

def find_similar_image(uploaded_image_path):
    uploaded_embedding = generate_embedding(uploaded_image_path)

    best_match = None
    highest_similarity = -1

    for image_path in REFERENCE_FOLDER.iterdir():
        if image_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        reference_embedding = generate_embedding(image_path)

        similarity = compare_embeddings(uploaded_embedding, reference_embedding)

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = image_path.name

    return {
        "best_match": best_match,
        "similarity": round(highest_similarity * 100, 2)
    }