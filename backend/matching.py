
"""Explainable, deterministic matching rules — not an LLM."""
from datetime import datetime
from typing import Any


def evaluate_recipients(
    donation: dict[str, Any],
    recipients: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Return eligible matches and rejected candidates with reasons."""
    category = str(donation["food_category"]).strip().casefold()
    quantity = float(donation["quantity_kg"])
    datetime.fromisoformat(donation["pickup_deadline"])

    if quantity <= 0:
        raise ValueError("Donation quantity must be greater than zero.")

    matches = []
    rejected = []

    for recipient in recipients:
        recipient_id = recipient["id"]
        name = recipient["organisation_name"]
        capacity = float(recipient["capacity_kg"])
        categories = {
            str(item).strip().casefold()
            for item in recipient["food_categories"]
        }

        reasons = []

        if category not in categories:
            reasons.append(
                f"Recipient does not accept the '{category}' category."
            )

        if capacity < quantity:
            reasons.append(
                f"Declared capacity ({capacity:g} kg) is below "
                f"the donation quantity ({quantity:g} kg)."
            )

        if capacity <= 0:
            reasons.append("Declared capacity must be greater than zero.")

        if reasons:
            rejected.append({
                "recipient_id": recipient_id,
                "organisation_name": name,
                "rejection_reasons": reasons,
            })
            continue

        capacity_fit = min(quantity / capacity, 1.0)
        score = round(70 + 30 * capacity_fit)

        matches.append({
            "recipient_id": recipient_id,
            "organisation_name": name,
            "location": recipient["location"],
            "score": score,
            "reasons": [
                "Food category matches the recipient's declared categories.",
                f"Declared capacity ({capacity:g} kg) meets the "
                f"donation quantity ({quantity:g} kg).",
                f"Capacity-fit component: {round(capacity_fit * 100)}%.",
                "Recipient must confirm availability and pickup timing.",
                "Food safety requires separate human verification.",
            ],
            "requires_human_review": True,
        })

    matches.sort(key=lambda item: (
        -item["score"],
        item["organisation_name"].casefold(),
    ))
    rejected.sort(key=lambda item: item["organisation_name"].casefold())

    return {
        "matches": matches,
        "rejected_candidates": rejected,
    }


def rank_recipients(
    donation: dict[str, Any],
    recipients: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Backward-compatible helper returning eligible matches only."""
    return evaluate_recipients(donation, recipients)["matches"]

