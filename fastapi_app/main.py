from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import client
from .routes import router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to MongoDB...")
    yield
    client.close()
    print("MongoDB connection closed.")

app = FastAPI(title="Nexus Board API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")