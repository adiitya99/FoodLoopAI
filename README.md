# FoodLoop AI
### Autonomous Food Rescue and Redistribution Agent

FoodLoop AI is a hackathon prototype designed to help coordinate surplus-food donations with recipient organisations in Kokrajhar, Assam.

## Problem
Surplus food can go unused while community organisations need food resources. Coordinating donors, recipient capacity, food categories and pickup timing can be difficult.

## Solution
FoodLoop AI provides a dashboard to record donations, register recipient organisations, evaluate potential matches and track donation workflow status.

## Key Features
- Donation listing with quantity, category, location and timing.
- Recipient registration with accepted food categories and declared capacity.
- Explainable, rule-based candidate matching.
- Reasons for eligible and rejected candidates.
- Donation status workflow with validated transitions.
- Agent decision logs and tool trace.
- Human review requirement for food safety and recipient confirmation.
- Streamlit dashboard and FastAPI backend.
- SQLite persistence.

## Architecture

```text
Donor / Recipient
       |
       v
Streamlit Dashboard
       |
       v
FastAPI Backend
       |
       +------> SQLite Database
       |
       v
Agent Orchestrator
       |
       +------> Retrieve recipients
       |
       +------> Evaluate category and capacity
       |
       +------> Record rationale and tool trace
       |
       v
Suggested matches for human review
```

## Technology Stack
- Python
- FastAPI
- Streamlit
- SQLite
- Pydantic
- Pytest

## Run Locally

Activate your virtual environment, then open two terminals.

### Terminal 1: Backend

```powershell
cd D:\FoodLoopAI_complete_starter\FoodLoopAI
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Backend health check: http://127.0.0.1:8000/health

API documentation: http://127.0.0.1:8000/docs

### Terminal 2: Frontend

```powershell
cd D:\FoodLoopAI_complete_starter\FoodLoopAI
python -m streamlit run frontend/app.py
```

Open the local URL printed in the terminal, usually http://localhost:8501.

## Run Tests

```powershell
python -m pytest -v
```

The current test suite covers matching rules and key donation status transitions.

## Safety and Limitations
- Matching is deterministic and rule-based, not an LLM-based autonomous decision.
- A proposed match does not mean the recipient has accepted the donation.
- Food safety is not certified by this system.
- Human verification and recipient confirmation remain necessary.
- The current prototype does not independently verify pickup, delivery or real-world partner participation.
- Matching currently uses declared food categories and capacity; it does not establish real-world suitability or travel distance.

## Project Status
Hackathon prototype. Demonstration data should not be represented as verified operational outcomes.
