from fastapi import FastAPI, UploadFile, File
from PIL import Image, ImageOps
from keras.models import load_model
from pydantic import BaseModel
from io import BytesIO
import uvicorn, numpy as np

URL_MODEL = './model/keras_model.h5'
URL_CLASS_NAMES = './model/labels.txt'
SIZE_IMAGE = (224, 224)

np.set_printoptions(suppress=True)

class InputImage(BaseModel):
    file: UploadFile

class PredictCar:
    def __init__(self):
        self.model =  self.load_model_car()
        self.class_names =  self.load_class_names()

    def load_model_car(self):
        return load_model(URL_MODEL, compile=False)
    
    def load_class_names(self):
        with open(URL_CLASS_NAMES, 'r') as file:
            return file.readlines()

    def create_data_to_predict(self, path_or_bytes_image):
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(BytesIO(path_or_bytes_image)).convert("RGB")
        image = ImageOps.fit(image, SIZE_IMAGE, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array
        return data

    def predict(self, path_or_bytes_image):
        data = self.create_data_to_predict(path_or_bytes_image)
        prediction = self.model.predict(data)
        return {
            'Классы' : ['2107', 'Granta', 'Niva'],
            'Процент схожести' : [str(prediction[0][0]), str(prediction[0][1]), str(prediction[0][2])]
        }

app = FastAPI()
predict_car = PredictCar()

@app.post('/get_predict')
async def get_predict(file: UploadFile = File(...)):
    file_read = await file.read()
    return predict_car.predict(file_read)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)