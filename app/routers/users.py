from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.team import Team
from app.models.user_team import UserTeam
import app.schemas.user as schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# CREATE - Crear usuario
@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def crear_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    
    # Verificar si el email ya existe
    user_existente = db.query(User).filter(User.email == user.email).first()
    if user_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el email '{user.email}'"
        )
    
    nuevo_user = User(
        nombre=user.nombre,
        email=user.email,
        activo=user.activo
    )
    
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)
    
    return nuevo_user

# READ - Listar usuarios
@router.get("/", response_model=List[schemas.User])
def listar_users(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    activo: bool = None,
    db: Session = Depends(get_db)
):
    """Listar usuarios con filtros opcionales."""
    
    query = db.query(User)
    
    # Filtro por búsqueda
    if search:
        query = query.filter(
            (User.nombre.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    # Filtro por estado
    if activo is not None:
        query = query.filter(User.activo == activo)
    
    users = query.offset(skip).limit(limit).all()
    return users

# READ - Obtener usuario por ID
@router.get("/{user_id}", response_model=schemas.User)
def obtener_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario específico."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    return user

# READ - Obtener usuario con sus equipos
@router.get("/{user_id}/teams")
def obtener_user_teams(user_id: int, db: Session = Depends(get_db)):
    """Obtener usuario con la lista de equipos a los que pertenece."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    # Query manual para obtener equipos del usuario
    teams_data = db.query(
        Team.id,
        Team.nombre,
        Team.descripcion,
        UserTeam.role,
        UserTeam.joined_at
    ).join(
        UserTeam, UserTeam.team_id == Team.id
    ).filter(
        UserTeam.user_id == user_id
    ).all()
    
    teams = [
        {
            "team_id": t.id,
            "nombre": t.nombre,
            "descripcion": t.descripcion,
            "role": t.role,
            "joined_at": t.joined_at
        }
        for t in teams_data
    ]
    
    return {
        "user": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "activo": user.activo
        },
        "teams": teams,
        "total_teams": len(teams)
    }

# UPDATE - Actualizar usuario
@router.put("/{user_id}", response_model=schemas.User)
def actualizar_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un usuario existente."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    # Actualizar campos
    if user_data.nombre is not None:
        user.nombre = user_data.nombre
    
    if user_data.email is not None:
        # Verificar que el email no esté en uso
        email_existente = db.query(User).filter(
            User.email == user_data.email,
            User.id != user_id
        ).first()
        
        if email_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email '{user_data.email}' ya está en uso"
            )
        
        user.email = user_data.email
    
    if user_data.activo is not None:
        user.activo = user_data.activo
    
    db.commit()
    db.refresh(user)
    
    return user

# DELETE - Eliminar usuario
@router.delete("/{user_id}")
def eliminar_user(user_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    nombre_user = user.nombre
    
    # Eliminar relaciones con equipos primero
    db.query(UserTeam).filter(UserTeam.user_id == user_id).delete()
    
    # Eliminar usuario
    db.delete(user)
    db.commit()
    
    return {
        "mensaje": f"Usuario '{nombre_user}' eliminado correctamente",
        "id": user_id
    }

# POST - Agregar usuario a equipo
@router.post("/{user_id}/teams/{team_id}")
def agregar_user_a_team(
    user_id: int,
    team_id: int,
    role: str = "member",
    db: Session = Depends(get_db)
):
    """Agregar un usuario a un equipo."""
    
    # Verificar que existan
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    
    # Verificar si ya está en el equipo
    relacion_existente = db.query(UserTeam).filter(
        UserTeam.user_id == user_id,
        UserTeam.team_id == team_id
    ).first()
    
    if relacion_existente:
        raise HTTPException(
            status_code=400,
            detail=f"{user.nombre} ya está en el equipo {team.nombre}"
        )
    
    # Crear relación
    nueva_relacion = UserTeam(
        user_id=user_id,
        team_id=team_id,
        role=role
    )
    
    db.add(nueva_relacion)
    db.commit()
    
    return {
        "mensaje": f"{user.nombre} agregado a {team.nombre} como {role}",
        "user_id": user_id,
        "team_id": team_id,
        "role": role
    }

# DELETE - Remover usuario de equipo
@router.delete("/{user_id}/teams/{team_id}")
def remover_user_de_team(
    user_id: int,
    team_id: int,
    db: Session = Depends(get_db)
):
    """Remover un usuario de un equipo."""
    
    relacion = db.query(UserTeam).filter(
        UserTeam.user_id == user_id,
        UserTeam.team_id == team_id
    ).first()
    
    if not relacion:
        raise HTTPException(
            status_code=404,
            detail="El usuario no está en ese equipo"
        )
    
    db.delete(relacion)
    db.commit()
    
    return {
        "mensaje": "Usuario removido del equipo correctamente",
        "user_id": user_id,
        "team_id": team_id
    }