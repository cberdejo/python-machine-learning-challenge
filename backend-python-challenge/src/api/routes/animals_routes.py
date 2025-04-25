from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from minio import Minio

from api.models.generic_response import GenericResponse
from api.controllers.animals_controller import (
    fetch_and_store_animal_data,
)

router = APIRouter(prefix="/api/v1/animals", tags=["data"])


@router.post(
    "/",
)
async def store_animal_data(
    request: Request, seed: int = 42, number_of_datapoints: int = 1000
):
    return await fetch_and_store_animal_data(request, seed, number_of_datapoints)
