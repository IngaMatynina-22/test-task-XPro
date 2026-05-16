from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import init_db


from src.category.router import router as category_router
from src.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Catalog API",
    version="1.0.0",
    description="API for managing product catalog categories and products.",
    lifespan=lifespan,
)

app.include_router(category_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}