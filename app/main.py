from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tasks API",
    description="Sistema de gestión de tareas en equipo",
    version="1.0.0"
)

# CORS (para que puedas hacer un frontend después)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Tasks API - Sistema de gestión de tareas",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}