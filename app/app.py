import time

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
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
    print(arr)
    return np.array(arr)


def get_predictions(input):
    data_payload = input.astype(np.float32)
    prediction = Session.run(None, {Input_name: data_payload})[0]
    return prediction


REQUEST_COUNT = Counter(
    "total_app_requests", "Total number of requets", ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(
    "application_request_duration",
    "Time to complete requests",
    ["method", "path"],
    buckets=(0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1, 2, 5, 10),
)

REQUEST_ERROR = Counter(
    "application_request_error",
    "Total Number of request erros",
    ["method", "path", "status"],
)

REQUEST_QUEUE = Gauge(
    "application_request_in_queue", "Current number of requsts pending"
)


@app.middleware("http")
async def count_requests(request, call_next):
    REQUEST_QUEUE.inc()
    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 500
        raise
    finally:
        end_time = time.time()
        REQUEST_QUEUE.dec()
        REQUEST_LATENCY.labels(method=request.method, path=request.url.path).observe(
            end_time - start_time
        )
        REQUEST_COUNT.labels(
            method=request.method, path=request.url.path, status=status
        ).inc()

        if status >= 400:
            REQUEST_ERROR.labels(
                method=request.method, path=request.url.path, status=status
            ).inc()

    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


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
        return {"prediction": float(prediction[0][0])}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
