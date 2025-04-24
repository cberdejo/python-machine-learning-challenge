from typing import List
from api.models.animal_data import AnimalData
from api.models.generic_response import GenericResponse
from api.models.synthetic_data import SyntheticDataParams
from api.utils import (
    get_model_deserialized_from_minio,
    save_prediction_to_minio,
)
from config.minio_config import BUCKET_PREDICTIONS, BUCKET_MODELS
from fastapi import Request
from fastapi.responses import JSONResponse
from machine_learning.predict import predict
from machine_learning.models.analysis_result import AnalysisResult
from minio import Minio
import logging
import os

logger = logging.getLogger(__name__)


async def predict_controller(
    request: Request, model: SyntheticDataParams, animal_data: List[AnimalData]
):
    response = GenericResponse(code=500, message="Something went wrong", data=None)

    minio_client: Minio = request.app.state.minio_client
    object_path = f"{model.seed}-{model.number_of_datapoints}/model.pkl"

    # Try to get the model from MinIO

    try:
        model, label_encoder = get_model_deserialized_from_minio(
            minio_client, BUCKET_MODELS, object_path
        )
    except FileNotFoundError:
        logger.warning("Model not found in MinIO")
        response.code = 404
        response.message = f"Model not found in MinIO, use train endpoint to train a model: {os.getenv('HOST', '0.0.0.0')}:8000/api/v1/train?seed={model.seed}&number_of_datapoints={model.number_of_datapoints}"
        response.data = None
        return JSONResponse(status_code=response.code, content=response.model_dump())
    except Exception as e:
        logger.error(f"Error fetching model from MinIO: {str(e)}")
        response.code = 500
        response.message = f"Error validating model: {str(e)}"
        return JSONResponse(status_code=response.code, content=response.model_dump())

    # predict
    try:
        result: List[AnimalData] = predict(
            animal_data, model, label_encoder=label_encoder
        )
        response.data = result
        response.message = "Prediction successfully done."
        response.code = 200
        response.data = result
        save_prediction_to_minio(minio_client, BUCKET_PREDICTIONS, model, result)
        return JSONResponse(status_code=response.code, content=response.model_dump())
    except Exception as e:
        logger.error(f"Error validating model: {str(e)}")
        response.code = 500
        response.message = f"Error validating model: {str(e)}"
        return JSONResponse(status_code=response.code, content=response.model_dump())
