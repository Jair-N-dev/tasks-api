from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TeamBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)

class Team(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TeamWithStats(Team):
    """Team con estadísticas adicionales"""
    total_members: int = 0
    total_tasks: int = 0