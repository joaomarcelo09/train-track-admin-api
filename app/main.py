from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, trains, lines, tracks, simulation
from .database.connection import connect_to_mongo, close_mongo_connection
from .core.config import settings

app = FastAPI(title="Train Track Admin API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(auth.router, prefix="/api")
app.include_router(trains.router, prefix="/api")
app.include_router(lines.router, prefix="/api")
app.include_router(tracks.router, prefix="/api")
app.include_router(simulation.router, prefix="/api")
app.include_router(simulation.router)

@app.get("/")
async def root():
    return {"message": "Train Track Admin API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
