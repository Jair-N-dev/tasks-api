from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Importar TODOS los modelos
from app.models.team import Team
from app.models.user import User
from app.models.user_team import UserTeam

# Crear tablas
Base.metadata.create_all(bind=engine)

# Importar routers
from app.routers import teams, users

app = FastAPI(
    title="Tasks API",
    description="Sistema de gestión de tareas en equipo",
    version="1.0.0"
)

# CORS
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
        "status": "online",
        "endpoints": {
            "teams": "/teams",
            "users": "/users",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

# Registrar routers
app.include_router(teams.router)
app.include_router(users.router)