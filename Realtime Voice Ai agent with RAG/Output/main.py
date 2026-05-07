from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import equipment, stream

logger.remove()
logger.add(sys.stdout, colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan> - <level>{message}</level>")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RAG Voice AI Agent backend...")
    await connect_to_mongo()
    yield
    logger.info("Shutting down...")
    await close_mongo_connection()

app = FastAPI(
    title="RAG Voice AI Agent API",
    description="Realtime Voice AI Agent with RAG - Colab Demo",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"])

app.include_router(equipment.router, prefix="/api/v1/equipment", tags=["Equipment"])
app.include_router(stream.router,    prefix="/api/v1/stream",    tags=["Stream"])

@app.get("/")
def read_root():
    return {"message": "RAG Voice AI Agent API is running", "version": "0.1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
