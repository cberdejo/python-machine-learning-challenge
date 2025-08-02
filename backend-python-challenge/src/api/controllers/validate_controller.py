from api.models.generic_response import GenericResponse
from api.models.synthetic_data import SyntheticDataParams
from api.utils import (
    get_data_from_minio_by_seed_and_number_datapoints,
    get_model_deserialized_from_minio,
)
from config.minio_config import BUCKET_DATA, BUCKET_MODELS
from fastapi import Request
from fastapi.responses import JSONResponse
from machine_learning.models.analysis_result import AnalysisResult
from machine_learning.validate import validate
from minio import Minio
import logging
import os

logger = logging.getLogger(__name__)


async def validate_controller(
    request: Request, model: SyntheticDataParams, data: SyntheticDataParams
):
    """
    Validate the model using the data provided.
    Args:
        request (Request): The FastAPI request object.
        model (SyntheticDataParams): Model parameters.
        data (SyntheticDataParams): Data parameters.
    Returns:
        JSONResponse: Response containing the validation results.
    """
    response = GenericResponse(code=500, message="Something went wrong", data=None)

    minio_client: Minio = request.app.state.minio_client
    object_path = f"{model.seed}-{model.number_of_datapoints}/model.pkl"

    # Try to get the model from MinIO

    try:
        trained_model, _ = get_model_deserialized_from_minio(
            minio_client, BUCKET_MODELS, object_path
        )
    except FileNotFoundError:
        logger.warning("Model not found in MinIO")
        response.code = 404
        response.message = f"Model not found in MinIO, use train endpoint to train a model: {settings.HOST}:{settings.port}/api/v1/train?seed={model.seed}&number_of_datapoints={model.number_of_datapoints}"
        response.data = None
        return JSONResponse(status_code=response.code, content=response.model_dump())
    except Exception as e:
        logger.error(f"Error fetching model from MinIO: {str(e)}")
        response.code = 500
        response.message = f"Error validating model: {str(e)}"
        return JSONResponse(status_code=response.code, content=response.model_dump())

    # Try to get the data from MinIO
    try:
        dataframe = await get_data_from_minio_by_seed_and_number_datapoints(
            data.seed, data.number_of_datapoints, minio_client, BUCKET_DATA
        )
    except Exception as e:
        logger.error(f"Error fetching data from MinIO: {str(e)}")
        response.code = 500
        response.message = f"Error fetching data: {str(e)}"
        response.data = None
        return JSONResponse(status_code=response.code, content=response.model_dump())
    # Validate
    try:
        result: AnalysisResult = validate(dataframe, trained_model)
        response.data = result.model_dump(exclude={"model"})
        response.message = "Model validated successfully."
        response.code = 200
        response.data = result
        return JSONResponse(status_code=response.code, content=response.model_dump())
    except Exception as e:
        logger.error(f"Error validating model: {str(e)}")
        response.code = 500
        response.message = f"Error validating model: {str(e)}"
        return JSONResponse(status_code=response.code, content=response.model_dump())
