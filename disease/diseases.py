from fastapi import APIRouter
from schemas.suicide_schema import suicide_queriesEntity
from pydantic import BaseModel
import pickle
from fastapi import FastAPI, File, UploadFile
from keras.preprocessing import image
import numpy as np
import os

parkinsons_query_router  = APIRouter(
    prefix="/disease",
    tags=['Diseases']
)   

parkinsons_model = pickle.load(open("./disease/parkinsons_model.pickle",mode='rb'))

upload_dir = "uploads"  # You can change this directory as needed

# Ensure the directory exists or create it if it doesn't
os.makedirs(upload_dir, exist_ok=True)


def load_sample(path):
    
    img_path =  path
    
    img = image.load_img(img_path, target_size=(300, 300))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    print("Image shape : ",img_tensor.shape)
    return img_tensor




@parkinsons_query_router.post("/parkinsons")
async def upload_image(image: UploadFile):
    filename = f"{upload_dir}/{image.filename}"
    with open(filename, "wb") as image_file:
        image_data = image.file.read()
        image_file.write(image_data)
        tensor = load_sample(filename)
        output = parkinsons_model.predict(tensor)[0]
        print(output)
        prob = 0
        class_predicted = ""
        if output[0]>output[1]:
            prob = output[0]
            class_predicted = "Healthy"
        else:
            prob = output[1]
            class_predicted = "Parkinsons"
            
    return {"message": "Image uploaded successfully","pred":str(prob),"class_predicted":str(class_predicted)}


