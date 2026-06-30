from sqlalchemy import Column, Integer, String, DateTime, Text
from backend.db.database import Base
import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    correlation_id = Column(String, index=True)
    agent_id = Column(String, index=True)
    tool_name = Column(String)
    parameters = Column(Text)
    risk_score = Column(Integer)
    decision = Column(String)  # GREEN, YELLOW, RED
    mitre_mappings = Column(String)
    owasp_mappings = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String) # ALLOWED, BLOCKED, SUSPENDED, PENDING_REVIEW, APPROVED, REJECTED
    admin_notes = Column(Text, nullable=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)