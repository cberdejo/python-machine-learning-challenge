import os
from api.models.generic_response import GenericResponse
from clustering.cluster_data import cluster_and_label_data, label_dataset_no_clustering

from fastapi import Request
from fastapi.responses import JSONResponse
import httpx
from minio import Minio
from config.minio_config import BUCKET_DATA
import logging
import io
import polars as ps

logger = logging.getLogger(__name__)
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data_service:8777")


def save_dataset_as_datafile(data: list[dict]) -> io.BytesIO:
    """
    Converts the dataset to a CSV format and saves it in memory.
    Args:
        data (list[dict]): List of dictionaries containing animal data.
    returns:
        io.BytesIO: In-memory CSV file.

    """
    df = ps.DataFrame(data)

    columns = ["height", "weight", "walks_on_n_legs", "has_wings", "has_tail", "label"]

    df = df[columns]

    buffer = io.StringIO()
    df.write_csv(buffer)

    byte_data = io.BytesIO(buffer.getvalue().encode("utf-8"))
    return df, byte_data


async def process_and_store_data(
    minio_client: Minio, seed: int, number_of_datapoints: int
) -> ps.DataFrame:
    """
    Fetches animal data from the API, labels it, and stores it in Minio.
    Args:
        minio_client (Minio): Minio client instance for object storage.
        seed (int): Seed for random number generation.
        number_of_datapoints (int): Number of data points to generate.
    Returns:
            DataFrame: DataFrame containing the labeled animal data.
    Raises:
        Exception: If there is an error fetching data from the API or storing it in Minio.
    """

    # url = "http://localhost:8777/api/v1/animals/data"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {"seed": seed, "number_of_datapoints": number_of_datapoints}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATA_SERVICE_URL}/api/v1/animals/data", headers=headers, json=payload
        )

        if response.status_code == 200:
            logger.info("Data received successfully from the API.")

            # Labeling the dataset
            data = label_dataset_no_clustering(response.json())
            df, file_data = save_dataset_as_datafile(data)

            # Working progress
            dataframe = ps.DataFrame(response.json())
            cluster_and_label_data(dataframe)

            # Get date and time
            file_name = f"{seed}-{number_of_datapoints}/animal_data.data"
            try:
                minio_client.put_object(
                    BUCKET_DATA,
                    file_name,
                    file_data,
                    length=file_data.getbuffer().nbytes,
                    content_type="text/plain",
                )

            except Exception as e:
                logger.error(f"Error storing data in Minio: {str(e)}")
                raise e
        else:
            logger.error(
                f"Error fetching data from API: {response.status_code} - {response.text}"
            )
            raise Exception(
                f"Error fetching data from API: {response.status_code} - {response.text}"
            )
    return df


async def fetch_and_store_animal_data(
    request: Request, seed: int, number_of_datapoints: int
):
    """
    Fetches animal data from the API, labels it, and stores it in Minio.
    Args:
        request (Request): FastAPI request object.
        seed (int): Seed for random number generation.
        number_of_datapoints (int): Number of data points to generate.
    Returns:
        JSONResponse: JSON response with the status of the operation.
    """
    minio_client: Minio = request.app.state.minio_client
    response = GenericResponse(
        code=200,
        message="Animal data received successfully.",
        data={"seed": seed, "number_of_datapoints": number_of_datapoints},
    )

    try:
        df: ps.DataFrame = await process_and_store_data(
            minio_client, seed, number_of_datapoints
        )
        response.data["data_first_ten"] = df.head(10).to_dicts()
        logger.info(f"Generated {len(df)} data points for seed {seed}")
    except Exception as e:
        response.code = 500
        response.message = f"Error processing data: {str(e)}"
        response.data = None

    return JSONResponse(status_code=response.code, content=response.model_dump())
