from pydantic import BaseModel
from datetime import datetime

class UserTeamBase(BaseModel):
    user_id: int
    team_id: int
    role: str = "member"

class UserTeamCreate(UserTeamBase):
    pass

class UserTeam(UserTeamBase):
    id: int
    joined_at: datetime
    
    class Config:
        from_attributes = True

class TeamMember(BaseModel):
    """Info de un miembro en un equipo"""
    user_id: int
    nombre: str
    email: str
    role: str
    joined_at: datetime