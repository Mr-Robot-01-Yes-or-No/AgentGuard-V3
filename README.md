<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,100:00FF9C&height=200&section=header&text=AGENTGUARD%20V3&fontSize=55&fontColor=00FF9C&animation=fadeIn&fontAlignY=38&desc=Enterprise%20Zero-Trust%20Enforcement%20Proxy%20for%20Autonomous%20AI%20Agents&descAlignY=55&descSize=16" width="100%"/>

<img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=20&duty=800&pause=1000&color=00FF9C&center=true&vCenter=true&width=700&lines=Real-time+Risk+Scoring+for+Autonomous+Agent+Actions;Policy-as-Code+%2B+Human-in-the-Loop+Enforcement;Zero+Trust+by+Default.+No+Silent+Agent+Actions." alt="Typing SVG" />

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-0D1117?style=flat-square&logo=python&logoColor=00FF9C&labelColor=0D1117)
![License](https://img.shields.io/badge/License-MIT-0D1117?style=flat-square&labelColor=0D1117&color=00FF9C)
![Status](https://img.shields.io/badge/Status-Active-0D1117?style=flat-square&labelColor=0D1117&color=00FF9C)
![PRs](https://img.shields.io/badge/PRs-Welcome-0D1117?style=flat-square&labelColor=0D1117&color=00FF9C)

</div>

<br>

## `> overview`

**AgentGuard V3** is a zero-trust enforcement layer that sits between autonomous AI agents and the systems they act on. Every agent action is intercepted, scored against a real-time risk engine, evaluated by a policy engine, and — depending on severity — either auto-approved, blocked, or escalated to a human for review before execution.

Built for teams deploying LLM-based agents into production environments where unchecked tool calls, API invocations, or system actions carry real operational risk.

```yaml
core_principle: "Never trust an agent action by default — verify, score, and gate it."
enforcement_model: "Risk-scored, policy-gated, human-escalated"
target_use_case: "Autonomous agents with access to sensitive tools, APIs, or infrastructure"
```

<br>

## `> core_features`

<div align="center">

| Module | Description |
|---|---|
| 🔐 **Zero Trust Architecture** | Every agent request is authenticated and evaluated — no implicit trust, no default allow |
| ⚖️ **Risk Engine** | Real-time risk scoring of agent actions based on configurable signals and thresholds |
| 📋 **Policy Engine** | Declarative, policy-as-code rules governing what agents can and cannot do |
| 🧠 **Decision Engine** | Central arbiter that combines risk score + policy outcome into an allow/block/escalate decision |
| 🙋 **Human-in-the-Loop** | High-risk or ambiguous actions are routed to a human reviewer before execution |
| 🚨 **Incident Queue** | Centralized queue for flagged actions, reviews, and audit trail of decisions |
| 🤖 **AI Agent Simulator** | Built-in simulator to generate synthetic agent traffic for testing policies end-to-end |
| 🔑 **JWT Authentication** | Secure, token-based authentication for agents and dashboard access |

</div>

<br>

## `> tech_stack`

<div align="center">

**Backend & API**

![Python](https://img.shields.io/badge/Python-0D1117?style=for-the-badge&logo=python&logoColor=00FF9C)
![FastAPI](https://img.shields.io/badge/FastAPI-0D1117?style=for-the-badge&logo=fastapi&logoColor=00FF9C)
![JWT](https://img.shields.io/badge/JWT-0D1117?style=for-the-badge&logo=jsonwebtokens&logoColor=00FF9C)

**Data Layer**

![SQLite](https://img.shields.io/badge/SQLite-0D1117?style=for-the-badge&logo=sqlite&logoColor=00FF9C)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-0D1117?style=for-the-badge&logo=python&logoColor=00FF9C)

**Dashboard & Interface**

![Streamlit](https://img.shields.io/badge/Streamlit-0D1117?style=for-the-badge&logo=streamlit&logoColor=00FF9C)
![Swagger](https://img.shields.io/badge/Swagger%20UI-0D1117?style=for-the-badge&logo=swagger&logoColor=00FF9C)

</div>

<br>

## `> architecture`

<div align="center">

<img src="./docs/architecture.png" alt="AgentGuard V3 Architecture Diagram" width="85%">

*Agent request → JWT Auth → Risk Engine → Policy Engine → Decision Engine → (Auto-Execute | Human Review | Block) → Incident Queue*

</div>

<br>


## `> quickstart`

**1. Install dependencies**

```bash
git clone https://github.com/Ujas-Gohil-Cyber-Security/AgentGuard-V3.git
cd AgentGuard-V3
pip install -r requirements.txt
```

**2. Start the backend API (FastAPI)**

```bash
uvicorn backend.main:app --reload
```

API will be available at `http://localhost:8000` — interactive Swagger docs at `http://localhost:8000/docs`.

**3. Launch the dashboard (Streamlit)**

```bash
python -m streamlit run dashboard/app.py
```

**4. Run the AI agent simulator**

```bash
python simulator/agent_sim.py
```

This generates synthetic agent traffic against the running backend so you can observe risk scoring, policy evaluation, and human-in-the-loop escalation in real time.

<br>

## `> project_structure`
AgentGuard-V3/
├── backend/ # FastAPI application, risk/policy/decision engines
├── dashboard/ # Streamlit dashboard (incident queue, live logs)
├── simulator/ # AI agent traffic simulator
├── docs/ # Architecture diagram & screenshots
└── requirements.txt

<br>

## `> legal_disclaimer`

AgentGuard V3 is provided for **educational, research, and internal enforcement purposes**. It is not a certified security compliance product. Evaluate against your own organization's risk, compliance, and regulatory requirements before deploying in a production environment handling sensitive data or critical infrastructure.

<br>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,100:00FF9C&height=100&section=footer" width="100%"/>

`"Trust nothing. Verify everything. Escalate what matters."`

</div>
