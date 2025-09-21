from typing import List

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="APP")


class PredictionInput(BaseModel):
    Age: float
    Income: float
    Dependents: float
    Occupation: str
    Credit: float
    Property: str


occupation_dict = {"Employed": 0, "Self-Employed": 1, "Unemployed": 2}
property_dict = {"Apartment": 0, "Condo": 1, "House": 3}


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: PredictionInput):
    pass
