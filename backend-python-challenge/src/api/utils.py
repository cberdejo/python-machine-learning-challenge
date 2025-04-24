from io import BytesIO
from typing import List
from api.controllers.animals_controller import process_and_store_data
from api.models.animal_data import AnimalData
from minio import Minio
import polars as ps
import pickle
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def get_data_from_minio_by_seed_and_number_datapoints(
    seed: int, number_of_datapoints: int, minio_client, bucket_data: str
) -> ps.DataFrame:
    """
    Fetches data from MinIO using the provided seed and number of datapoints.
    If the data is not found, it generates new data and stores it in MinIO.

    Args:
        seed (int): The seed for generating data.
        number_of_datapoints (int): The number of datapoints to generate.
        minio_client: The MinIO client instance.
        BUCKET_DATA (str): The name of the MinIO bucket for data storage.

    Returns:
        pd.DataFrame: The fetched or generated data as a DataFrame.
    """
    object_path = f"{seed}-{number_of_datapoints}/animal_data.data"
    dataframe: ps.DataFrame = None
    try:
        data = minio_client.get_object(bucket_data, object_path)
        response_bytes = BytesIO(data.read())
        dataframe = ps.read_csv(response_bytes)
        logger.info(f"Data found in MinIO: {object_path}")

    except Exception as e:
        if "NoSuchKey" in str(e):
            logger.warning("Data not found in MinIO, generating new data...")
            dataframe = await process_and_store_data(
                minio_client, seed, number_of_datapoints
            )
        else:
            logger.error(f"Error fetching data from MinIO: {str(e)}")
            raise e
    return dataframe


def get_model_deserialized_from_minio(
    minio_client: Minio, bucket: str, object_path: str
):
    """
    Deserialize a model from MinIO.

    Args:
        minio_client (Minio): Configured MinIO client.
        bucket (str): Bucket where the model is stored.
        object_path (str): Path to the model within the bucket.

    Returns:
        The deserialized model.
    """

    try:
        response_obj = minio_client.get_object(bucket, object_path)
        model_bytes = response_obj.read()

        loaded = pickle.loads(model_bytes)
        model = loaded["model"]
        label_encoder = loaded["label_encoder"]

        return model, label_encoder
    except Exception as e:
        if "NoSuchKey" in str(e):
            logger.warning("Model not found in MinIO")
            raise FileNotFoundError("Model not found in MinIO")
        else:
            logger.error(f"Error fetching model from MinIO: {str(e)}")
            raise e


def save_prediction_to_minio(
    minio_client: Minio, bucket: str, model, result: List[AnimalData]
):
    """
    Save the prediction result to MinIO.
    Args:
        minio_client (Minio): Configured MinIO client.
        bucket (str): Bucket where the prediction will be stored.
        model: The model used for prediction.
        result (List[AnimalData]): The prediction result to be saved.
    """
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    object_path = f"{now}/prediction.data"
    try:
        # Convert the result to a DataFrame and save it as a CSV in memory
        df = ps.DataFrame(result)
        csv_buffer = BytesIO()
        df.write_csv(csv_buffer)
        csv_buffer.seek(0)

        # Upload the CSV to MinIO
        minio_client.put_object(
            bucket,
            object_path,
            csv_buffer,
            len(csv_buffer.getvalue()),
            content_type="text/csv",
        )
    except Exception as e:
        logger.error(f"Error saving prediction to MinIO: {str(e)}")
        raise e
