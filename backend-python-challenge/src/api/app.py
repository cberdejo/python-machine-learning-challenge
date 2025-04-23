from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.logger_config import setup_logging
import logging
from config.minio_config import MINIOCONFIG, setup_minio_buckets
from api.routes.animals_routes import router as animals_routes
from api.routes.machine_learning_routes import router as machine_learning_routes


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management with Minio"""
    logger.info("Connecting to Minio...")
    minio_client = MINIOCONFIG
    app.state.minio_client = minio_client
    logger.info("Minio connection established")

    try:
        setup_minio_buckets(minio_client)
    except Exception as e:
        logger.error(f"Minio setup failed: {str(e)}")
        raise e

    yield  # Wait until the application stops

    logger.info("Closing Minio connection...")
    del minio_client
    logger.info("Minio connection closed")


app = FastAPI(lifespan=lifespan)

app.include_router(animals_routes)
app.include_router(machine_learning_routes)
