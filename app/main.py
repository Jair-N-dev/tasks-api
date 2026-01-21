from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Importar modelos
from app.models.team import Team
from app.models.user import User
from app.models.user_team import UserTeam
from app.models.task import Task

# Crear tablas
Base.metadata.create_all(bind=engine)

# Importar routers
from app.routers import teams, users, tasks

# Metadata mejorada
app = FastAPI(
    title="Tasks API",
    description="""
    🚀 **Sistema completo de gestión de tareas en equipo**
    
    ## Características principales
    
    * **Teams**: Gestión de equipos de trabajo
    * **Users**: Administración de usuarios
    * **Tasks**: Sistema completo de tareas con estados y prioridades
    * **Relationships**: Relaciones muchos a muchos entre usuarios y equipos
    
    ## Autor
    
    Desarrollado por **[Jair]** - [GitHub](https://github.com/Jair-N-dev)
    """,
    version="1.0.0",
    contact={
        "name": "Jair",
        "url": "https://github.com/Jair-N-dev/tasks-api"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def root():
    """
    # 🏠 Bienvenido a Tasks API
    
    Sistema de gestión de tareas en equipo con FastAPI y MySQL.
    
    ## 📚 Recursos disponibles:
    - **Teams**: `/teams/` - Gestión de equipos
    - **Users**: `/users/` - Gestión de usuarios  
    - **Tasks**: `/tasks/` - Gestión de tareas
    
    ## 📖 Documentación:
    - **Swagger UI**: `/docs` (esta página)
    - **ReDoc**: `/redoc`
    
    ## ✨ Features:
    - Autenticación por roles
    - Filtros avanzados
    - Búsqueda full-text
    - Estadísticas en tiempo real
    """
    return {
        "message": "Tasks API - Sistema de gestión de tareas",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "teams": "/teams",
            "users": "/users",
            "tasks": "/tasks",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    🏥 Health check endpoint
    
    Verifica que la API y la base de datos estén funcionando correctamente.
    """
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

# Registrar routers
app.include_router(teams.router)
app.include_router(users.router)
app.include_router(tasks.router)