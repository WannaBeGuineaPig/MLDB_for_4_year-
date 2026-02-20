import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

from modul.connect_bd_module import *
from modul.predict_module import *

class InputData(BaseModel):
    comment: str
    true_type_comment: str

app = FastAPI()
predict_class_comment = PredictClassComment()

@app.get('/comment')
def comments_from_bd():
    data = get_comments_from_bd()
    return data 

@app.post('/predict-tonality-comment')
def predict_tonality_comment(request: InputData):
    predict_model_type, response_data = predict_class_comment.get_predict_tonality_comment(request.comment)
    save_data_bd(request.comment, request.true_type_comment, predict_model_type)
    return response_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)