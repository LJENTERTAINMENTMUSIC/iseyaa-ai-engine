"""
Run ISEYAA FastAPI server using uvicorn
"""
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("PORT", 8000))
    print(f"Starting ISEYAA AI Engine (FastAPI) on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
