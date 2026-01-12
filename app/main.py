from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.config.database import Base, engine
from app.routers.v1.auth_router import auth_router
from app.routers.v1.note_router import note_router
from app.routers.v1.voice_router import voice_router
from app.routers.v1.summerize_router import summarize_router
from app.config.database import Base, engine

# ---------------------- CREATE TABLES ----------------------
# This will create all tables defined in your SQLAlchemy models
Base.metadata.create_all(bind=engine)

# ---------------------- APP ----------------------
app = FastAPI()

# CORS
origins = [
    "http://localhost:5173",  # your frontend URL
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(note_router)
app.include_router(voice_router)
app.include_router(summarize_router)
