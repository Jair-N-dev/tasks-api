from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models.team import Team
import app.schemas.team as schemas

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

# CREATE - Crear equipo
@router.post("/", response_model=schemas.Team, status_code=status.HTTP_201_CREATED)
def crear_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo equipo.
    
    - **nombre**: Nombre único del equipo (requerido)
    - **descripcion**: Descripción opcional del equipo
    """
    # Verificar si ya existe
    team_existente = db.query(Team).filter(Team.nombre == team.nombre).first()
    if team_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un equipo con el nombre '{team.nombre}'"
        )
    
    nuevo_team = Team(
        nombre=team.nombre,
        descripcion=team.descripcion
    )
    
    db.add(nuevo_team)
    db.commit()
    db.refresh(nuevo_team)
    
    return nuevo_team

# READ - Listar todos los equipos
@router.get("/", response_model=List[schemas.Team])
def listar_teams(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar todos los equipos con paginación y búsqueda opcional.
    
    - **skip**: Registros a saltar (paginación)
    - **limit**: Número máximo de registros
    - **search**: Buscar por nombre (opcional)
    """
    query = db.query(Team)
    
    # Búsqueda opcional
    if search:
        query = query.filter(Team.nombre.ilike(f"%{search}%"))
    
    teams = query.offset(skip).limit(limit).all()
    return teams

# READ - Obtener equipo por ID
@router.get("/{team_id}", response_model=schemas.Team)
def obtener_team(team_id: int, db: Session = Depends(get_db)):
    """
    Obtener un equipo específico por ID.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {team_id} no encontrado"
        )
    
    return team

# READ - Obtener equipo con estadísticas
@router.get("/{team_id}/stats", response_model=schemas.TeamWithStats)
def obtener_team_stats(team_id: int, db: Session = Depends(get_db)):
    """
    Obtener equipo con estadísticas (total de miembros y tareas).
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {team_id} no encontrado"
        )
    
    # Preparar respuesta (por ahora sin estadísticas reales)
    # Las agregaremos cuando tengamos Users y Tasks
    team_dict = {
        "id": team.id,
        "nombre": team.nombre,
        "descripcion": team.descripcion,
        "created_at": team.created_at,
        "updated_at": team.updated_at,
        "total_members": 0,  # Lo calcularemos después
        "total_tasks": 0     # Lo calcularemos después
    }
    
    return team_dict

# UPDATE - Actualizar equipo
@router.put("/{team_id}", response_model=schemas.Team)
def actualizar_team(
    team_id: int,
    team_data: schemas.TeamUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un equipo existente.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {team_id} no encontrado"
        )
    
    # Actualizar solo los campos que se enviaron
    if team_data.nombre is not None:
        # Verificar que el nuevo nombre no exista
        nombre_existente = db.query(Team).filter(
            Team.nombre == team_data.nombre,
            Team.id != team_id
        ).first()
        
        if nombre_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otro equipo con el nombre '{team_data.nombre}'"
            )
        
        team.nombre = team_data.nombre
    
    if team_data.descripcion is not None:
        team.descripcion = team_data.descripcion
    
    db.commit()
    db.refresh(team)
    
    return team

# DELETE - Eliminar equipo
@router.delete("/{team_id}")
def eliminar_team(team_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un equipo.
    
    NOTA: Solo se puede eliminar si no tiene miembros ni tareas asociadas.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {team_id} no encontrado"
        )
    
    # TODO: Verificar que no tenga miembros ni tareas
    # (Lo agregaremos cuando tengamos esas tablas)
    
    nombre_team = team.nombre
    db.delete(team)
    db.commit()
    
    return {
        "mensaje": f"Equipo '{nombre_team}' eliminado correctamente",
        "id": team_id
    }

# STATS - Obtener estadísticas generales
@router.get("/stats/general")
def estadisticas_generales(db: Session = Depends(get_db)):
    """
    Obtener estadísticas generales de todos los equipos.
    """
    total_teams = db.query(func.count(Team.id)).scalar()
    
    return {
        "total_teams": total_teams,
        "total_members": 0,  # Lo calcularemos después
        "total_tasks": 0     # Lo calcularemos después
    }