import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.database import session_manager
from app.models import Base

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    Read https://fastapi.tiangolo.com/advanced/events/
    """
    # Temporario | create db tables
    async with session_manager.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
    logging.info("Starting lifecycle")
    try:
        yield
    finally:
        # await cleanup()
        logging.info("Ending lifecycle")


app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Demo",
    docs_url="/api/docs",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router, prefix="/api")
