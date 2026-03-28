"""TuVi AI — FastAPI Application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import db
from app.routers import profile
from app.services import scraper_browser

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    db.init_db()
    await scraper_browser.start()
    logger.info("TuVi AI backend started")
    yield
    await scraper_browser.shutdown()
    logger.info("TuVi AI backend stopped")


app = FastAPI(
    title="TuVi AI",
    description="Vietnamese astrology AI interpretation service",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
