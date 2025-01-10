import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))


app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)