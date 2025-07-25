from fastapi import FastAPI, HTTPException
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Backtesting SMA APIs",
    description="A FastAPI application for backtesting Simple Moving Average (SMA) trading strategies",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Backtesting SMA APIs - Server is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "API is running",
        "environment": os.getenv("ENV", "development")
    }

# CORS configuration - more flexible for production
origins = [
    "http://localhost:3000",      # React dev server
    "http://localhost:5173",      # Vite dev server
    "http://localhost:8000",      # Alternative dev port
    "https://dma-backtester.vercel.app",  # Production frontend
]

# Allow environment variable override
if os.getenv("ALLOWED_ORIGINS"):
    origins.extend(os.getenv("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return HTTPException(status_code=500, detail="Internal server error")

handler = Mangum(app)