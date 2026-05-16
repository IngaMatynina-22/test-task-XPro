from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import init_db


from src.category.router import router as category_router
from src.database import init_db

from src.product.router import router as product_router

from src.seed import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_database()
    yield


app = FastAPI(
    title="Catalog API",
    version="1.0.0",
    description="API for managing product catalog categories and products.",
    lifespan=lifespan,
)

app.include_router(category_router)
app.include_router(product_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}