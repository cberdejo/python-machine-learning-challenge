from api.models.generic_response import GenericResponse
from fastapi import Request
from fastapi.responses import JSONResponse
from minio import Minio
from config.minio_config import BUCKET_MODELS

async def get_all_models(request: Request) -> JSONResponse:
    """
    Get all models from the database.
    Args:
        request (Request): The FastAPI request object.
    Returns:
    """
    response: GenericResponse = GenericResponse(
        code=500, message="Something went wrong", data=None
    )

    minio_client: Minio = request.app.state.minio_client

    # Get the list of models from MinIO
    try:
        models = minio_client.list_objects(
            bucket_name=BUCKET_MODELS,
            prefix="",
            recursive=False,
        )
        # delete last character '/' from the path
        models_formatted = [model.object_name[:-1] for model in models]
        response.data = models_formatted
        response.code = 200
        response.message = "Models fetched successfully."
        return JSONResponse(status_code=response.code, content=response.model_dump())
    except Exception as e:
        response.code = 500
        response.message = f"Error fetching models from MinIO: {str(e)}"
        return JSONResponse(status_code=response.code, content=response.model_dump())
