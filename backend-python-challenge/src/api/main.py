import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main function to run the FastAPI application.
    """
    host = os.getenv("HOST", "0.0.0.0")  # Default to "0.0.0.0" if HOST is not set
    uvicorn.run(
        "api.app:app",
        reload=True,
        host=host,
        port=8000,
    )


if __name__ == "__main__":
    main()
