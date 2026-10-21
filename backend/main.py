"""FastAPI entry point for the FoodLoop AI prototype."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from . import database
from .schemas import (
    DonationCreate,
    RecipientCreate,
    DonationResponse,
    DonationStatusUpdate,
)
from .agent import process_donation


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize local database tables before serving requests."""
    database.init_db()
    yield


app = FastAPI(
    title="FoodLoop AI",
    description="Prototype for coordinating surplus food donations with recipient organisations.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    """Provide a welcome message."""
    return {"message": "Welcome to FoodLoop AI", "status": "running"}


@app.get("/health")
def health_check():
    """Return basic process health."""
    return {"status": "healthy"}


@app.post("/donations", response_model=DonationResponse, status_code=201)
def create_donation(payload: DonationCreate):
    """Save a donation and mark it for human review."""
    try:
        return database.create_donation(payload.model_dump(mode="json"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Could not save donation") from exc


@app.get("/donations")
def get_donations():
    """List donation records."""
    return database.list_donations()


@app.post("/recipients", status_code=201)
def create_recipient(payload: RecipientCreate):
    """Register a recipient organisation."""
    try:
        return database.create_recipient(payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Could not save recipient") from exc


@app.get("/recipients")
def get_recipients():
    """List active recipient organisations."""
    return database.list_recipients()


@app.post("/donations/{donation_id}/match")
def match_donation(donation_id: int):
    """Return candidate matches, never an automatic delivery confirmation."""
    donation = next((item for item in database.list_donations() if item["id"] == donation_id), None)
    if donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return process_donation(donation)


@app.get("/agent-runs")
def get_agent_runs():
    """Expose decision logs for the demo."""
    return database.list_agent_runs()

@app.patch("/donations/{donation_id}/status")
def update_donation_status(
    donation_id: int,
    payload: DonationStatusUpdate,
):
    """Update a donation's workflow status."""

    try:
        donation = database.update_donation_status(
            donation_id,
            payload.status,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if donation is None:
        raise HTTPException(
            status_code=404,
            detail="Donation not found",
        )

    return donation
