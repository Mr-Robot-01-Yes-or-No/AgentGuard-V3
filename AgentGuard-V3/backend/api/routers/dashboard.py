from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db.database import get_db
from backend.db.models import AuditLog
from backend.core.security import get_current_user
from backend.services.corporate_tools import CorporateToolsService
import json

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total = db.query(AuditLog).count()
    red = db.query(AuditLog).filter(AuditLog.decision == "RED").count()
    yellow = db.query(AuditLog).filter(AuditLog.decision == "YELLOW").count()
    green = db.query(AuditLog).filter(AuditLog.decision == "GREEN").count()
    pending = db.query(AuditLog).filter(AuditLog.status == "PENDING_REVIEW").count()
    return {"total": total, "red": red, "yellow": yellow, "green": green, "pending": pending}

@router.get("/incidents/pending")
def get_pending_incidents(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(AuditLog).filter(AuditLog.status == "PENDING_REVIEW").order_by(AuditLog.timestamp.desc()).all()

@router.get("/logs")
def get_all_logs(limit: int = 50, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()

@router.post("/incidents/{incident_id}/approve")
def approve_incident(incident_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    incident = db.query(AuditLog).filter(AuditLog.id == incident_id, AuditLog.status == "PENDING_REVIEW").first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found or not pending")
    
    incident.status = "APPROVED"
    incident.admin_notes = f"Approved by {current_user['sub']} - {incident.admin_notes}"
    db.commit()
    
    # Execute the action now that it's approved
    params = json.loads(incident.parameters)
    result = CorporateToolsService.execute(incident.tool_name, params)
    
    return {"status": "success", "message": "Incident approved and action executed", "result": result}

@router.post("/incidents/{incident_id}/reject")
def reject_incident(incident_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    incident = db.query(AuditLog).filter(AuditLog.id == incident_id, AuditLog.status == "PENDING_REVIEW").first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found or not pending")
    
    incident.status = "REJECTED"
    incident.admin_notes = f"Rejected by {current_user['sub']} - {incident.admin_notes}"
    db.commit()
    return {"status": "success", "message": "Incident rejected"}
