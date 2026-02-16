import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

from connect_bd_module import *
from predict_module import *

class InputData(BaseModel):
    comment: str

app = FastAPI()
predict_class_comment = PredictClassComment()

@app.get('/comment')
def comments_from_bd():
    data = get_comments_from_bd()
    return data 

@app.post('/predict-tonality-comment')
def predict_tonality_comment(request: InputData):
    data = predict_class_comment.get_predict_tonality_comment(request.comment)
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)