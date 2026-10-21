# Architecture

Version 0.1.0 starter proposal. Confirm behaviour by running tests.

- `frontend/app.py`: Streamlit donor/recipient and match UI.
- `backend/main.py`: FastAPI routes and request orchestration.
- `backend/schemas.py`: Pydantic input validation.
- `backend/database.py`: SQLite persistence.
- `backend/matching.py`: transparent category/capacity candidate filtering.
- `backend/agent.py`: fixed-order Python orchestration and rationale logging.

Trust boundaries:
- User input is untrusted.
- Match results are suggestions, not acceptance or delivery.
- Software does not certify food safety.
- No notifications or external service integrations are active.
