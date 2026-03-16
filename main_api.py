"""Entry point for the FastAPI dashboard server."""
import os

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=int(os.getenv("DASHBOARD_PORT", "8080")),
        reload=False,
    )
