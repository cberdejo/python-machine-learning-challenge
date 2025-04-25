from datetime import date
from sqlite3 import Date
from typing import Optional
from api.controllers.get_all_models_controller import get_all_models
from api.controllers.get_predictions_controller import get_predictions_by_time_period
from api.models.animal_data import PredictRequest
from api.models.synthetic_data import ValidateRequest
from fastapi import APIRouter, Query, Request

from api.controllers.validate_controller import validate_controller
from api.controllers.predict_controller import predict_controller
from api.controllers.train_controller import train_model_controller


router = APIRouter(
    prefix="/api/v1/mpc", tags=["machine-learning"]
)


@router.get("/models")
async def get_models(request: Request):
    return await get_all_models(request)


@router.get("/predictions")
async def get_predictions(
    request: Request,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
):
    return await get_predictions_by_time_period(request, start, end)


@router.post("/train")
async def train_model(
    request: Request, seed: int = 42, number_of_datapoints: int = 1000
):
    return await train_model_controller(request, seed, number_of_datapoints)


@router.post("/validate")
async def validate(request: Request, payload: ValidateRequest):
    return await validate_controller(request, payload.model, payload.data)


@router.post("/predict")
async def predict(request: Request, payload: PredictRequest):
    return await predict_controller(request, payload.model, payload.data)
