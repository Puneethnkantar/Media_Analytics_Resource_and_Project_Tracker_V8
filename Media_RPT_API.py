import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Resource Tracker API")

# Setup CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory for the application
BASE_DIR = Path(__file__).resolve().parent

# Ensure data.json path
DATA_FILE = BASE_DIR / "data.json"

@app.get("/api/data")
async def get_data():
    """
    Endpoint to provide the application data from data.json.
    """
    try:
        if not DATA_FILE.exists():
            raise FileNotFoundError(f"Data file not found at {DATA_FILE}")
            
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return JSONResponse(content=data)
    except FileNotFoundError as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail="Data file not found. Please ensure data.json exists.")
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing data.json: {e}")
        raise HTTPException(status_code=500, detail="Error parsing data file. Invalid JSON format.")
    except Exception as e:
        logger.error(f"Unexpected error loading data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while loading data.")

# Mount the static files pointing to the current directory to serve the frontend.
# E.g. / will serve index.html, /app.js will serve app.js
app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Make sure to run the app with unvicorn Media_RPT_API:app --reload
    uvicorn.run("Media_RPT_API:app", host="0.0.0.1", port=8000, reload=True)
