from io import BytesIO
import pickle
from api.models.generic_response import GenericResponse
from api.utils import get_data_from_minio_by_seed_and_number_datapoints
from fastapi import Request
from fastapi.responses import JSONResponse
from minio import Minio, S3Error
from api.controllers.animals_controller import process_and_store_data
from config.minio_config import BUCKET_DATA
import logging
from machine_learning.classify import classify_data_using_hard_voting
from machine_learning.models.analysis_result import AnalysisResult
from config.minio_config import BUCKET_MODELS
import json
import io

logger = logging.getLogger(__name__)


def save_metrics_as_json(
    result: AnalysisResult, path: str, minio_client: Minio, bucket: str
):
    """
    Save evaluation metrics as a JSON file in MinIO.

    Args:
        result (AnalysisResult): Object containing model results.
        path (str): Path within the bucket (e.g., '123-500/metrics.json').
        minio_client (Minio): Configured MinIO client.
        bucket (str): Bucket where the file will be saved.
    """

    # Convertir a dict y serializar
    data = result.model_dump(exclude={"model"})
    json_bytes = json.dumps(data, indent=4).encode("utf-8")
    buffer = io.BytesIO(json_bytes)

    minio_client.put_object(
        bucket, path, buffer, length=len(json_bytes), content_type="application/json"
    )


async def train_model_controller(
    request: Request, seed: int, number_of_datapoints: int
):
    """
    Train a model using where the data is generated with the provided seed and number of datapoints, and store it in MinIO.
    Args:
        request (Request): The FastAPI request object.
        seed (int): Seed for random number generation.
        number_of_datapoints (int): Number of data points to generate.
    Returns:
        JSONResponse: Response containing the status of the training process.
    """

    response = GenericResponse(
        code=200,
        message="Model training completed successfully.",
        data={"seed": seed, "number_of_datapoints": number_of_datapoints},
    )

    minio_client: Minio = request.app.state.minio_client
    try:
        dataframe = await get_data_from_minio_by_seed_and_number_datapoints(
            seed, number_of_datapoints, minio_client, BUCKET_DATA
        )
    except Exception as e:
        logger.error(f"Error fetching data from MinIO: {str(e)}")
        response.code = 500
        response.message = f"Error fetching data: {str(e)}"
        response.data = None
        return JSONResponse(status_code=response.code, content=response.model_dump())

    try:
        # Entrenar el modelo
        results, label_encoder = classify_data_using_hard_voting(dataframe)

        model_package = {"model": results.model, "label_encoder": label_encoder}
        # Guardar el modelo
        model_buffer = BytesIO()
        pickle.dump(model_package, model_buffer)
        model_buffer.seek(0)

        initial_path = f"{seed}-{number_of_datapoints}"
        model_path = f"{initial_path}/model.pkl"
        metrics_path = f"{initial_path}/metrics.json"

        minio_client.put_object(
            BUCKET_MODELS,
            model_path,
            model_buffer,
            len(model_buffer.getvalue()),
        )

        # Guardar las métricas
        save_metrics_as_json(results, metrics_path, minio_client, BUCKET_MODELS)

        # Incluir resumen en la respuesta
        response.data["metrics"] = {
            "accuracy": results.accuracy,
            "precision": results.precision,
            "recall": results.recall,
            "f1": results.f1,
            "confusion_matrix": results.confusion_matrix,
        }

    except Exception as e:
        logger.error(f"Error storing model or metrics in MinIO: {str(e)}")
        response.code = 500
        response.message = f"Error training model: {str(e)}"
        response.data = None

    return JSONResponse(status_code=response.code, content=response.model_dump())
