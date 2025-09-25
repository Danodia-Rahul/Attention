import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class PredictionInput(BaseModel):
    Age: float
    Income: float
    Dependents: float
    Occupation: str
    Credit: float
    Property: str


occupation_dict = {"Employed": 0, "Self-Employed": 1, "Unemployed": 2}
property_dict = {"Apartment": 0, "Condo": 1, "House": 3}

Session = ort.InferenceSession("model.onnx")

Input_name = Session.get_inputs()[0].name


def convert_to_numpy_arr(data: PredictionInput):
    occupation_code = occupation_dict[data.Occupation]
    property_code = property_dict[data.Property]

    arr = [
        [
            data.Age,
            data.Income,
            data.Dependents,
            occupation_code,
            data.Credit,
            property_code,
        ]
    ]
    return np.array(arr)


def get_predictions(input):
    data_payload = input.astype(np.float32)
    prediction = Session.run(None, {Input_name: data_payload})[0]

    return prediction


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: PredictionInput):
    try:
        input = convert_to_numpy_arr(data)
        prediction = get_predictions(input)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
