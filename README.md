# 🛡️ AgentGuard V3

Enterprise Zero-Trust Enforcement Proxy for Autonomous AI Agents

## Features
- Zero Trust Architecture
- Risk Engine
- Policy Engine
- Decision Engine
- Human-in-the-Loop
- Incident Queue
- AI Agent Simulator
- JWT Authentication

## Tech Stack

Python
FastAPI
Streamlit
SQLite
SQLAlchemy
JWT

## Architecture

(image)

## Screenshots

Dashboard

Incident Queue

Live Logs

Swagger

## Installation

pip install -r requirements.txt

uvicorn backend.main:app --reload

python -m streamlit run dashboard/app.py

python simulator/agent_sim.py
