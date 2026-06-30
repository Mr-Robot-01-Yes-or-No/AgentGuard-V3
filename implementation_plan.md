# AgentGuard V3 - Implementation Plan

An enterprise-grade Zero Trust Enforcement Proxy for Autonomous AI Agents. This plan outlines the architecture, module responsibilities, APIs, data flow, security implications, edge cases, and testing strategy.

## Goal Description

Modern AI Agents have excessive agency, posing significant security risks if prompted maliciously (OWASP LLM01, OWASP LLM08). AgentGuard V3 operates as an enforcement gateway between AI Agents and Enterprise Tools. By applying Zero Trust principles, every request is evaluated by a Policy Engine and a Risk Engine. Safe actions (Green) proceed, medium-risk actions (Yellow) are logged and monitored, and high-risk actions (Red) are suspended pending human (Administrator) review in a SOC dashboard.

## Decisions Made
- **Database**: PostgreSQL / SQLite as the backend database.
- **Mappings**: Standard mappings (e.g. OWASP LLM01, LLM08) will be hardcoded in the Risk Engine.
- **Deployment**: The mock AI agent and corporate backend will be mocked within the same backend for simplicity of this initial build.

---

## Proposed Architecture

```mermaid
graph TD
    A[AI Agent (Untrusted)] -->|Tool Request| B(AgentGuard Proxy)
    
    subgraph AgentGuard Backend [FastAPI - Zero Trust Gateway]
        B --> C{Policy Engine}
        C --> D{Risk Engine}
        D -->|MITRE/OWASP Mapping| E{Decision Engine}
        
        E -->|GREEN| F[Execute API/Tool]
        E -->|YELLOW| G[Log & Execute]
        E -->|RED| H[Suspend & Queue]
    end
    
    G --> F
    
    F --> I[Corporate Tool Layer]
    H -->|Pending Approval| J[Database / SIEM]
    
    subgraph SOC Platform [Streamlit Dashboard]
        K[Security Admin] -->|JWT Auth| L(Admin Console)
        L -->|Approve/Reject| H
        J -.->|Live Logs/KPIs| L
    end
    
    I -.->|Response| B
    B -.->|Final Response| A
```

## Module Responsibilities

### 1. AgentGuard Backend (FastAPI)
The core proxy and decision-making system.
*   **Proxy Endpoint**: Authenticates agent requests, generates correlation IDs, and acts as the reverse proxy to internal tools.
*   **Policy Engine**: Evaluates requests against predefined enterprise policies (e.g., "no writes to `/etc/`", "no DROP TABLE queries").
*   **Risk Engine**: Calculates a risk score (0-100) based on payload, target, and context. Maps threats to MITRE ATT&CK and OWASP Top 10 for LLMs.
*   **Decision Engine**: Categorizes requests into GREEN, YELLOW, RED based on risk score and policies.
*   **Auth & Security**: Manages JWTs, RBAC for the SOC dashboard, and ensures the Proxy endpoint itself is secure.
*   **Observability**: Generates structured JSON logs, metrics (Prometheus), and handles distributed tracing contexts.

### 2. SOC Dashboard (Streamlit)
The frontend interface for security analysts and administrators.
*   **Executive KPIs**: High-level metrics (e.g., total requests blocked, active agents, risk distribution).
*   **Live SIEM**: Real-time structured log viewer with filtering.
*   **Incident Queue**: Displays RED actions waiting for manual approval. Allows admins to Approve, Reject, Quarantine, or Terminate.
*   **Threat Details**: Displays in-depth context on suspended requests, including correlation IDs, parameters, and MITRE/OWASP mappings.

### 3. Corporate Tool Layer (Mocked Services)
The simulated enterprise environment.
*   **Database**: Mock customer/order DB.
*   **Filesystem & Terminal**: Mock interfaces to simulate OS-level commands and file I/O.
*   **Internal APIs**: Mock HR, Finance, or operational APIs.

### 4. Core Agent Simulator
A script/service that generates synthetic traffic.
*   Fires safe requests (e.g., "read public docs").
*   Fires prompt injection attacks.
*   Attempts unauthorized database access or terminal commands to trigger YELLOW and RED workflows.

---

## Data Flow (Request Lifecycle)
1. **Intercept**: Agent makes an HTTP request to `POST /api/v1/proxy/execute`.
2. **Identify**: AgentGuard authenticates the agent (API Key/Token) and attaches a UUID correlation ID.
3. **Analyze**: The Policy Engine and Risk Engine parse the request payload (tool name, parameters).
4. **Decide**: 
   * **GREEN**: Forwards immediately to Corporate Tool Layer.
   * **YELLOW**: Writes detailed audit log, then forwards.
   * **RED**: Writes audit log, creates a `PendingApproval` record in DB, and holds the HTTP request open (or returns a `202 Accepted` pending status) until the Admin reviews via the Dashboard.
5. **Enforce**: Admin decision from the Dashboard updates the `PendingApproval` record, unblocking the Proxy to either execute the tool or return a security block message to the Agent.
6. **Return**: The final result (tool output or denial message) is returned to the Agent.

---

## Proposed Changes

### `backend/` (FastAPI)
- **[NEW]** `backend/main.py`: Application entry point, CORS, Prometheus middleware.
- **[NEW]** `backend/api/routers/proxy.py`: Endpoints for agent tool interception.
- **[NEW]** `backend/api/routers/dashboard.py`: Endpoints for the Streamlit SOC UI (incident queue, approval logic).
- **[NEW]** `backend/api/routers/auth.py`: JWT issuing and validation.
- **[NEW]** `backend/core/security.py`: JWT, hashing, RBAC enforcement.
- **[NEW]** `backend/core/config.py`: Pydantic BaseSettings for environment variables.
- **[NEW]** `backend/engines/policy_engine.py`: Rules evaluation logic.
- **[NEW]** `backend/engines/risk_engine.py`: Scoring and MITRE/OWASP mappings.
- **[NEW]** `backend/engines/decision_engine.py`: GREEN/YELLOW/RED logic aggregator.
- **[NEW]** `backend/db/`: SQLAlchemy/SQLModel models for `AuditLog`, `PendingApproval`, `Agent`.
- **[NEW]** `backend/services/corporate_tools.py`: Mock internal services execution layer.

### `dashboard/` (Streamlit)
- **[NEW]** `dashboard/app.py`: Entry point, routing, and dark mode configuration.
- **[NEW]** `dashboard/pages/01_KPIs.py`: High-level metrics.
- **[NEW]** `dashboard/pages/02_Incident_Queue.py`: Approval console for RED requests.
- **[NEW]** `dashboard/pages/03_Live_Logs.py`: SIEM-like log viewer.
- **[NEW]** `dashboard/components/auth.py`: Login form and JWT management.

### `simulator/`
- **[NEW]** `simulator/agent_sim.py`: Async script using `httpx` to send continuous varied traffic (Safe, Medium, Attacks) to the Proxy.

### `deployment/`
- **[NEW]** `docker-compose.yml`: Services for backend, dashboard, database.
- **[NEW]** `backend.Dockerfile` & `dashboard.Dockerfile`.

---

## Security Implications & Edge Cases

*   **Fail Secure**: If the Policy Engine crashes or the DB is unreachable, the system must default to RED (Deny) rather than bypassing checks.
*   **Concurrency & Timeouts**: If a RED request is pending, the HTTP connection might time out. 
    *   *Mitigation*: The proxy should ideally return an immediate "Request Suspended, Correlation ID: X" rather than hanging the HTTP connection, or implement long-polling/WebSockets. For this project, returning a structured HTTP 403 or 202 indicating "Pending Human Review" is the safest approach.
*   **Prompt Injection in Dashboard**: If the Agent's malicious payload includes XSS or Markdown exploits, displaying it in the Streamlit dashboard could compromise the SOC Analyst.
    *   *Mitigation*: All agent inputs must be strictly sanitized and rendered as raw text/JSON in the dashboard, never executed or rendered as raw HTML.
*   **Audit Trail Immutability**: Logs should be append-only.

---

## Verification Plan

### Automated Tests
- `pytest` for the engines:
  - Unit tests for Policy Engine (verifying rule evaluation).
  - Unit tests for Risk Engine (validating expected scores for prompt injections).
  - Unit tests for Decision Engine.
- Integration tests for the Proxy endpoint (ensuring GREEN executes, RED creates an incident).

### Manual Verification
- Deploy via `docker-compose up`.
- Run `agent_sim.py` to generate traffic.
- Login to the Streamlit SOC Dashboard.
- Verify that safe requests are logged as GREEN.
- Verify that destructive commands (e.g., `rm -rf /`) are flagged RED, appear in the Incident Queue, and can be manually Approved or Rejected.
- Verify that the Dashboard correctly displays MITRE/OWASP mappings and correlation IDs.
