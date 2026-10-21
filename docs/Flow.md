# Execution Flow

Startup: Uvicorn imports `backend.main:app`; FastAPI lifespan initializes SQLite tables.

Donation: `POST /donations` → Pydantic `DonationCreate` validation → `database.create_donation` → row saved as `pending_review` with human-review flag.

Matching: `POST /donations/{id}/match` → locate donation → `agent.process_donation` → `database.list_recipients` → `matching.rank_recipients` → log action, rationale and tool calls → return candidates requiring human review.

UI: Streamlit sends HTTP requests to `http://127.0.0.1:8000`; backend must run in another terminal.
