import uvicorn
from dotenv import load_dotenv
from config.settings import settings

def main():
    """
    Main function to run the FastAPI application.
    """

    uvicorn.run(
        "api.app:app",
        reload=True,
        host=settings.HOST,
        port=settings.PORT,
    )


if __name__ == "__main__":
    main()
