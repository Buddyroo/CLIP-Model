from fastapi import FastAPI, HTTPException, UploadFile, File
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from io import BytesIO
import torch
from typing import List, Optional

clip_id = 'laion/CLIP-ViT-g-14-laion2B-s12B-b42K'
clip_model = CLIPModel.from_pretrained(clip_id)
processor = CLIPProcessor.from_pretrained(clip_id)

app = FastAPI()

@app.post("/encode")
async def encode(images: List[UploadFile] = File(...)):
    image_inputs = []

    for image_file in images:
        image = Image.open(BytesIO(await image_file.read()))
        image_input = processor(images=image, return_tensors="pt")
        image_inputs.append(image_input["pixel_values"])

    if image_inputs:
        with torch.no_grad():
            image_features = clip_model.get_image_features(torch.cat(image_inputs, dim=0))
            features = image_features.mean(dim=0, keepdim=True)
            features /= features.norm(dim=-1, keepdim=True)
            return {"features": features.tolist()}
    else:
        raise HTTPException(status_code=404, detail="No valid images provided.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CLIP API. Use /encode for image encoding."}
