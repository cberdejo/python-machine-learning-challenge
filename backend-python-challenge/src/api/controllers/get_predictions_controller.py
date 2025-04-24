from datetime import date, datetime
from io import StringIO
from typing import Optional
from api.models.animal_data import AnimalData, Prediction
from api.models.generic_response import GenericResponse
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from minio import Minio
from config.minio_config import BUCKET_PREDICTIONS
import polars as ps


async def get_predictions_by_time_period(
    request: Request, start: Optional[date], end: Optional[date]
) -> JSONResponse:
    """
    Get predictions by time period.
    Args:
        request: The request object.
        start: The start date of the time period.
        end: The end date of the time period.
    Returns:
        A JSON response with the predictions for the specified time period.
    """
    response: GenericResponse = GenericResponse(
        code=500,
        message="Internal Server Error",
        data=None,
    )
    try:
        # Get the database connection from the request state
        minio_client: Minio = request.app.state.minio_client

        objects = minio_client.list_objects(
            bucket_name=BUCKET_PREDICTIONS,
            prefix="",
            recursive=True,
        )

        # Filter the predictions based on the time period
        predictions_filtered = []

        for obj in objects:
            try:
                obj_date_str = obj.object_name.split("/")[0]
                obj_date = datetime.strptime(obj_date_str, "%Y-%m-%d_%H-%M-%S").date()
            except Exception:
                continue  # Fecha inválida en el nombre

            if start and obj_date < start:
                continue
            if end and obj_date > end:
                continue

            # Leer el archivo prediction.data

            try:
                obj_data = minio_client.get_object(BUCKET_PREDICTIONS, obj.object_name)
                content = obj_data.read().decode("utf-8").strip()

                if not content:
                    continue

                df = ps.read_csv(StringIO(content))

                animal_list = [
                    AnimalData(
                        walks_on_n_legs=row["walks_on_n_legs"],
                        height=row["height"],
                        weight=row["weight"],
                        has_wings=row["has_wings"],
                        has_tail=row["has_tail"],
                        label=row.get("label"),
                    )
                    for row in df.to_dicts()
                ]

                prediction = Prediction(date=obj_date_str, animal_data=animal_list)
                predictions_filtered.append(prediction)
            except Exception as e:
                continue

        # If no predictions are found, return a 204 response
        if not predictions_filtered:
            return Response(status_code=204)
        # Return the predictions as a JSON response
        response.code = 200
        response.message = "Predictions retrieved successfully."
        response.data = predictions_filtered
        return JSONResponse(status_code=response.code, content=response.dict())

    except Exception as e:
        response.code = 500
        response.message = str(e)
        return JSONResponse(status_code=response.code, content=response.dict())
