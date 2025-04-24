import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main function to run the FastAPI application.
    """
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "api.app:app",
        reload=True,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    main()
