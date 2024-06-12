import json
import os
import requests
import logging

def process_video_data(video_id):
    url = "http://127.0.0.1:8000/encode"
    json_file_path = 'video_description/all_videos.json'
    frames_dir = "frames"

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_videos = json.load(file)

    video_url = all_videos.get(video_id, {}).get('url', None)
    text = all_videos.get(video_id, {}).get('description', None)

    files = []
    file_handles = []
    try:
        for filename in os.listdir(frames_dir):
            if filename.startswith(f'key_frame_{video_id}_') and filename.endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(frames_dir, filename)
                file_handle = open(file_path, 'rb')
                files.append(('images', (filename, file_handle, 'image/jpeg')))
                file_handles.append(file_handle)

        data = {'texts': [text]}

        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            #vector = response.json().get('features', None)
            result = response.json()
            vector = result.get('features', None)
            info = result.get('info', None)
            result = True
        else:
            log_message = f"Failed to get a proper response. Status code: {response.status_code}\nResponse: {response.text}"
            print(log_message)
            logging.error(log_message)
            vector = None
            result = False
            info = None
    except Exception as e:
        log_message = f"Error during data processing: {str(e)}"
        print(log_message)
        logging.error(log_message)
        vector = None
        result = False
        info = None
    finally:
        for file_handle in file_handles:
            file_handle.close()

    return info, result, vector

def delete_frames(folder, video_id):
    for filename in os.listdir(folder):
        if filename.startswith(f'key_frame_{video_id}_') and filename.endswith(('.jpg', '.jpeg', '.png')):
            os.remove(os.path.join(folder, filename))
    log_message = "All frames have been deleted."
    print(log_message)
    logging.info(log_message)



#print(process_video_data('2252e44042798abe3c2fe7e64392'))


from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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
async def encode(images: List[UploadFile] = File(default=[]), texts: List[str] = Form(None)):
    image_inputs = []
    text_inputs = {}
    info = []

    if images:  # Проверка наличия изображений
        for image_file in images:
            image = Image.open(BytesIO(await image_file.read()))
            image_input = processor(images=image, return_tensors="pt")
            image_inputs.append(image_input["pixel_values"])

    if texts:
        text_inputs = processor(text=texts, return_tensors="pt", padding=True, truncation=True)

    image_features, text_features = None, None

    if image_inputs:
        with torch.no_grad():
            image_features = clip_model.get_image_features(torch.cat(image_inputs, dim=0))
            info.append(f"Image features shape: {image_features.shape}")  # Добавляем информацию о размере признаков изображения
            image_features = image_features.mean(dim=0, keepdim=True)
            info.append(f"Mean image features shape: {image_features.shape}")  # Добавляем информацию о размере средних признаков изображения

    if text_inputs:
        with torch.no_grad():
            text_features = clip_model.get_text_features(**text_inputs)
            info.append(f"Text features shape: {text_features.shape}")  # Добавляем информацию о размере признаков текста
            text_features = text_features.mean(dim=0, keepdim=True)
            info.append(f"Mean text features shape: {text_features.shape}")  # Добавляем информацию о размере средних признаков текста

    if image_features is not None and text_features is not None:
        features = torch.cat((image_features, text_features), dim=1)
        info.append(f"Combined features shape (images and texts): {features.shape}")  # Добавляем информацию о размере объединенных признаков
        features /= features.norm(dim=-1, keepdim=True)
    elif image_features is not None:
        features = image_features
        info.append(f"Final image features shape: {features.shape}")  # Добавляем информацию о размере признаков изображения
    elif text_features is not None:
        features = text_features
        info.append(f"Final text features shape: {features.shape}")  # Добавляем информацию о размере признаков текста
    else:
        return {"features": None, "info": info}  # Возвращаем None и информацию, если нет ни изображений, ни текстов

    return {"info": info,"features": features.squeeze(0).tolist()}

@app.get("/")
def read_root():
    return {"message": "Welcome to the CLIP API. Use /encode for image and text encoding."}




