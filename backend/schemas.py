
"""Validated request and response schemas for the FoodLoop AI API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DonationCreate(BaseModel):
    """Fields submitted by a donor for a surplus-food listing."""

    model_config = ConfigDict(str_strip_whitespace=True)

    food_name: str = Field(min_length=2, max_length=100)
    quantity_kg: float = Field(gt=0, le=10000)
    food_category: str = Field(min_length=2, max_length=50)
    location: str = Field(min_length=2, max_length=200)
    prepared_at: datetime
    pickup_deadline: datetime
    storage_notes: str = Field(min_length=2, max_length=500)

    @model_validator(mode="after")
    def validate_deadline(self):
        """Ensure the pickup deadline is after the preparation time."""
        if self.pickup_deadline <= self.prepared_at:
            raise ValueError(
                "pickup_deadline must be after prepared_at"
            )
        return self


class RecipientCreate(BaseModel):
    """Fields describing an organisation that may receive donations."""

    model_config = ConfigDict(str_strip_whitespace=True)

    organisation_name: str = Field(min_length=2, max_length=150)
    food_categories: list[str] = Field(min_length=1)
    capacity_kg: float = Field(gt=0, le=10000)
    location: str = Field(min_length=2, max_length=200)
    contact_name: str = Field(min_length=2, max_length=100)


class DonationResponse(BaseModel):
    """Public representation of a donation record."""

    id: int
    food_name: str
    quantity_kg: float
    food_category: str
    location: str
    status: str
    requires_human_review: bool


class DonationStatusUpdate(BaseModel):
    """Request schema for updating a donation's workflow status."""

    status: Literal[
        "pending_review",
        "match_proposed",
        "accepted",
        "completed",
        "cancelled",
    ]
