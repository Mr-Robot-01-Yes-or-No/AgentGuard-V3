from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
import json
from backend.db.database import get_db
from backend.db.models import AuditLog
from backend.engines.policy_engine import PolicyEngine
from backend.engines.risk_engine import RiskEngine
from backend.engines.decision_engine import DecisionEngine
from backend.services.corporate_tools import CorporateToolsService
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/proxy", tags=["proxy"])

class ToolRequest(BaseModel):
    tool_name: str
    parameters: dict
    agent_id: str = "agent-001"

@router.post("/execute")
def execute_tool(request: ToolRequest, db: Session = Depends(get_db)):
    correlation_id = str(uuid.uuid4())
    
    # 1. Analyze
    policy_violations = PolicyEngine.evaluate(request.tool_name, request.parameters)
    risk_data = RiskEngine.calculate_risk(request.tool_name, request.parameters)
    
    # 2. Decide
    decision, reason = DecisionEngine.make_decision(policy_violations, risk_data)
    
    status_val = "ALLOWED"
    if decision == "RED":
        status_val = "PENDING_REVIEW"
        
    # 3. Log
    log_entry = AuditLog(
        correlation_id=correlation_id,
        agent_id=request.agent_id,
        tool_name=request.tool_name,
        parameters=json.dumps(request.parameters),
        risk_score=risk_data["score"],
        decision=decision,
        mitre_mappings=risk_data["mitre"],
        owasp_mappings=risk_data["owasp"],
        status=status_val,
        admin_notes=reason
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    # 4. Enforce
    if decision == "GREEN":
        result = CorporateToolsService.execute(request.tool_name, request.parameters)
        return {"correlation_id": correlation_id, "decision": decision, "result": result}
        
    elif decision == "YELLOW":
        result = CorporateToolsService.execute(request.tool_name, request.parameters)
        return {"correlation_id": correlation_id, "decision": decision, "warning": reason, "result": result}
        
    elif decision == "RED":
        # Suspend and queue
        return {"correlation_id": correlation_id, "decision": decision, "message": "Request suspended pending human review.", "reason": reason}
