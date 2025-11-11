import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pandas as pd
from fastapi import FastAPI, UploadFile
from PIL import Image, ImageOps
from keras.models import load_model
import uvicorn, numpy as np


URL_MODEL = './model/modelNN.h5'
URL_CLASS_NAMES = './model/class_names.txt'
SIZE_IMAGE = (28, 28)

np.set_printoptions(suppress=True)

class PredictDigit:
    def __init__(self):
        self.model =  self.load_model_digit()
        self.class_names =  self.load_class_names()

    def load_model_digit(self):
        return load_model(URL_MODEL, compile=False)
    
    def load_class_names(self):
        with open(URL_CLASS_NAMES, 'r') as file:
            return file.read().split(',')

    def create_data_to_predict(self, bytes_image):
        image = Image.frombytes('RGBA', (284, 284), bytes_image).convert('L')
        image = ImageOps.fit(image, (28, 28), Image.Resampling.LANCZOS)
        image_array = (np.asarray([image]).astype(np.float64) / 255)
        return image_array

    def predict(self, bytes_image):
        data = self.create_data_to_predict(bytes_image)
        prediction = self.model.predict(data)
        return pd.DataFrame({
            'Классы' : self.class_names,
            'Процент схожести' : [float(pred) for pred in prediction[0]]
        }).sort_values(by=['Процент схожести'], ascending=False)

app = FastAPI()
predict_car = PredictDigit()

@app.post('/predict')
async def predict(image: UploadFile):
    return predict_car.predict(await image.read())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)