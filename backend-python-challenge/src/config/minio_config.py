from minio import Minio, S3Error
import logging
from dotenv import load_dotenv
import os

load_dotenv()


logger = logging.getLogger(__name__)

BUCKET_MODELS = "models"
BUCKET_DATA = "data"
BUCKET_PREDICTIONS = "predictions"


MINIOCONFIG = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)


def setup_minio_buckets(client: Minio):
    """Create required buckets if they don't exist.
    Args:
        client (Minio): Minio client instance.
    Raises:
        S3Error: If there is an error creating or verifying the bucket.
    """
    for bucket in [BUCKET_MODELS, BUCKET_DATA, BUCKET_PREDICTIONS]:
        try:
            if not client.bucket_exists(bucket):
                logger.info(f"Bucket '{bucket}' not found. Creating it...")
                client.make_bucket(bucket)
                logger.info(f"Bucket '{bucket}' created successfully.")
            else:
                logger.info(f"Bucket '{bucket}' already exists.")
        except S3Error as e:
            logger.error(f"Failed to create or verify bucket '{bucket}': {str(e)}")
            raise
