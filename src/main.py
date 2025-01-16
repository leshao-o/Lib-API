import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.author import router as router_author
from src.api.auth import router as router_auth
from src.api.user import router as router_user


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_author)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
