from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table, String
from datetime import datetime
from app.database import Base

class UserTeam(Base):
    __tablename__ = "user_teams"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), default="member")  # member, admin, owner
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)