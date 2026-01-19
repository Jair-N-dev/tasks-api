from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.team import Team
from app.models.user import User
import app.schemas.task as schemas

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# CREATE - Crear tarea
@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def crear_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva tarea.
    
    - **team_id**: ID del equipo (requerido)
    - **asignado_a**: ID del usuario asignado (opcional)
    """
    # Verificar que el equipo exista
    team = db.query(Team).filter(Team.id == task.team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {task.team_id} no encontrado"
        )
    
    # Verificar que el usuario exista (si se asignó)
    if task.asignado_a:
        user = db.query(User).filter(User.id == task.asignado_a).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {task.asignado_a} no encontrado"
            )
    
    nueva_task = Task(
        titulo=task.titulo,
        descripcion=task.descripcion,
        prioridad=task.prioridad,
        team_id=task.team_id,
        asignado_a=task.asignado_a,
        due_date=task.due_date
    )
    
    db.add(nueva_task)
    db.commit()
    db.refresh(nueva_task)
    
    return nueva_task

# READ - Listar tareas con filtros
@router.get("/", response_model=List[schemas.TaskWithDetails])
def listar_tasks(
    skip: int = 0,
    limit: int = 100,
    team_id: Optional[int] = Query(None, description="Filtrar por equipo"),
    asignado_a: Optional[int] = Query(None, description="Filtrar por usuario asignado"),
    estado: Optional[schemas.TaskStatusEnum] = Query(None, description="Filtrar por estado"),
    prioridad: Optional[schemas.TaskPriorityEnum] = Query(None, description="Filtrar por prioridad"),
    search: Optional[str] = Query(None, description="Buscar en título o descripción"),
    db: Session = Depends(get_db)
):
    """
    Listar tareas con múltiples filtros opcionales.
    """
    # Query con JOINs para obtener detalles
    query = db.query(
        Task,
        Team.nombre.label("team_nombre"),
        User.nombre.label("asignado_nombre"),
        User.email.label("asignado_email")
    ).join(
        Team, Team.id == Task.team_id
    ).outerjoin(  # LEFT JOIN para usuarios (puede ser NULL)
        User, User.id == Task.asignado_a
    )
    
    # Aplicar filtros
    if team_id:
        query = query.filter(Task.team_id == team_id)
    
    if asignado_a:
        query = query.filter(Task.asignado_a == asignado_a)
    
    if estado:
        query = query.filter(Task.estado == estado)
    
    if prioridad:
        query = query.filter(Task.prioridad == prioridad)
    
    if search:
        query = query.filter(
            or_(
                Task.titulo.ilike(f"%{search}%"),
                Task.descripcion.ilike(f"%{search}%")
            )
        )
    
    # Paginación
    results = query.offset(skip).limit(limit).all()
    
    # Formatear respuesta
    tasks = []
    for row in results:
        task_dict = {
            "id": row.Task.id,
            "titulo": row.Task.titulo,
            "descripcion": row.Task.descripcion,
            "estado": row.Task.estado,
            "prioridad": row.Task.prioridad,
            "team_id": row.Task.team_id,
            "asignado_a": row.Task.asignado_a,
            "created_at": row.Task.created_at,
            "updated_at": row.Task.updated_at,
            "due_date": row.Task.due_date,
            "completed_at": row.Task.completed_at,
            "team_nombre": row.team_nombre,
            "asignado_nombre": row.asignado_nombre,
            "asignado_email": row.asignado_email
        }
        tasks.append(task_dict)
    
    return tasks

# READ - Obtener tarea por ID
@router.get("/{task_id}", response_model=schemas.TaskWithDetails)
def obtener_task(task_id: int, db: Session = Depends(get_db)):
    """
    Obtener una tarea específica con detalles.
    """
    result = db.query(
        Task,
        Team.nombre.label("team_nombre"),
        User.nombre.label("asignado_nombre"),
        User.email.label("asignado_email")
    ).join(
        Team, Team.id == Task.team_id
    ).outerjoin(
        User, User.id == Task.asignado_a
    ).filter(
        Task.id == task_id
    ).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    task_dict = {
        "id": result.Task.id,
        "titulo": result.Task.titulo,
        "descripcion": result.Task.descripcion,
        "estado": result.Task.estado,
        "prioridad": result.Task.prioridad,
        "team_id": result.Task.team_id,
        "asignado_a": result.Task.asignado_a,
        "created_at": result.Task.created_at,
        "updated_at": result.Task.updated_at,
        "due_date": result.Task.due_date,
        "completed_at": result.Task.completed_at,
        "team_nombre": result.team_nombre,
        "asignado_nombre": result.asignado_nombre,
        "asignado_email": result.asignado_email
    }
    
    return task_dict

# UPDATE - Actualizar tarea
@router.put("/{task_id}", response_model=schemas.Task)
def actualizar_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una tarea existente.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    # Actualizar campos
    if task_data.titulo is not None:
        task.titulo = task_data.titulo
    
    if task_data.descripcion is not None:
        task.descripcion = task_data.descripcion
    
    if task_data.estado is not None:
        task.estado = task_data.estado
        
        # Si se marca como completada, guardar fecha
        if task_data.estado == schemas.TaskStatusEnum.COMPLETED and not task.completed_at:
            task.completed_at = datetime.utcnow()
        
        # Si se desmarca de completada, limpiar fecha
        if task_data.estado != schemas.TaskStatusEnum.COMPLETED:
            task.completed_at = None
    
    if task_data.prioridad is not None:
        task.prioridad = task_data.prioridad
    
    if task_data.asignado_a is not None:
        # Verificar que el usuario exista
        user = db.query(User).filter(User.id == task_data.asignado_a).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {task_data.asignado_a} no encontrado"
            )
        task.asignado_a = task_data.asignado_a
    
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    
    db.commit()
    db.refresh(task)
    
    return task

# DELETE - Eliminar tarea
@router.delete("/{task_id}")
def eliminar_task(task_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una tarea.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    titulo_task = task.titulo
    db.delete(task)
    db.commit()
    
    return {
        "mensaje": f"Tarea '{titulo_task}' eliminada correctamente",
        "id": task_id
    }

# PATCH - Cambiar estado de tarea
@router.patch("/{task_id}/estado")
def cambiar_estado_task(
    task_id: int,
    nuevo_estado: schemas.TaskStatusEnum,
    db: Session = Depends(get_db)
):
    """
    Cambiar solo el estado de una tarea (atajo).
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    estado_anterior = task.estado
    task.estado = nuevo_estado
    
    # Marcar fecha de completado
    if nuevo_estado == schemas.TaskStatusEnum.COMPLETED:
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None
    
    db.commit()
    db.refresh(task)
    
    return {
        "mensaje": f"Estado cambiado de '{estado_anterior}' a '{nuevo_estado}'",
        "task_id": task_id,
        "nuevo_estado": nuevo_estado
    }

# PATCH - Asignar/reasignar tarea
@router.patch("/{task_id}/asignar/{user_id}")
def asignar_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Asignar una tarea a un usuario.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    task.asignado_a = user_id
    db.commit()
    
    return {
        "mensaje": f"Tarea '{task.titulo}' asignada a {user.nombre}",
        "task_id": task_id,
        "user_id": user_id
    }

# GET - Estadísticas de tareas
@router.get("/stats/general")
def estadisticas_tasks(db: Session = Depends(get_db)):
    """
    Obtener estadísticas generales de tareas.
    """
    total = db.query(func.count(Task.id)).scalar()
    
    por_estado = db.query(
        Task.estado,
        func.count(Task.id)
    ).group_by(Task.estado).all()
    
    por_prioridad = db.query(
        Task.prioridad,
        func.count(Task.id)
    ).group_by(Task.prioridad).all()
    
    return {
        "total_tasks": total,
        "por_estado": {estado: count for estado, count in por_estado},
        "por_prioridad": {prioridad: count for prioridad, count in por_prioridad}
    }