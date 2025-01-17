import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.author import router as router_author
from src.api.auth import router as router_auth
from src.api.user import router as router_user
from src.api.book import router as router_book
from src.api.borrow import router as router_borrow
from src.logger import logger


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_author)
app.include_router(router_book)
app.include_router(router_borrow)

if __name__ == "__main__":
    logger.info("Запуск приложения через uvicorn")
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
