import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import v1_api_router
from app.core.database import session_manager
from app.models import Base

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Function that handles startup and shutdown events.

    Read https://fastapi.tiangolo.com/advanced/events
    """

    # Temporario | create db tables
    async with session_manager.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)

    logging.info("Starting lifecycle")
    try:
        yield
    finally:
        await session_manager.close()
        logging.info("Ending lifecycle")


app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Demo",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(v1_api_router, prefix="/api")
