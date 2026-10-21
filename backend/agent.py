
"""FoodLoop AI's deterministic, explainable agent workflow."""

from typing import Any

from .database import (
    list_recipients,
    log_agent_run,
    update_donation_status,
)
from .matching import evaluate_recipients


def process_donation(donation: dict[str, Any]) -> dict[str, Any]:
    """Evaluate recipients, propose matches, and log the decision."""

    tool_log = []
    donation_id = donation.get("id")

    # Step 1: Retrieve eligible recipient records.
    recipients = list_recipients()

    tool_log.append({
        "tool": "list_recipients",
        "result_count": len(recipients),
        "reason": (
            "Recipient categories and declared capacities are needed "
            "before matching."
        ),
    })

    # Step 2: Evaluate candidates against matching rules.
    evaluation = evaluate_recipients(donation, recipients)
    matches = evaluation["matches"]
    rejected_candidates = evaluation["rejected_candidates"]

    tool_log.append({
        "tool": "evaluate_recipients",
        "eligible_count": len(matches),
        "rejected_count": len(rejected_candidates),
        "reason": (
            "Check declared category compatibility and capacity, "
            "and explain why candidates do or do not qualify."
        ),
    })

    # Step 3: Propose matches without confirming a food handoff.
    if matches:
        action = "proposed_matches"
        rationale = (
            f"Found {len(matches)} eligible candidate(s) and "
            f"{len(rejected_candidates)} rejected candidate(s). "
            "Suggestions require human review, food-safety checks, "
            "and recipient confirmation."
        )

        # Update the status only if the current transition is allowed.
        if donation_id is not None:
            try:
                updated_donation = update_donation_status(
                    donation_id,
                    "match_proposed",
                )
                if updated_donation is not None:
                    donation["status"] = updated_donation["status"]
                    tool_log.append({
                        "tool": "update_donation_status",
                        "result": updated_donation["status"],
                        "reason": (
                            "Eligible matches were found; a match was "
                            "proposed for human review."
                        ),
                    })
            except ValueError as exc:
                # Preserve the matching result without forcing an invalid
                # workflow transition.
                tool_log.append({
                    "tool": "update_donation_status",
                    "result": "not_updated",
                    "reason": str(exc),
                })
    else:
        action = "no_match"
        rationale = (
            "No recipient met the current category and capacity rules. "
            f"{len(rejected_candidates)} candidate(s) were evaluated. "
            "Rejection reasons are included for human review."
        )

    # Step 4: Log the agent's decision and tool activity.
    log_agent_run(
        donation_id,
        action,
        rationale,
        tool_log,
    )

    return {
        "donation_id": donation_id,
        "action": action,
        "rationale": rationale,
        "matches": matches,
        "rejected_candidates": rejected_candidates,
        "status": donation.get("status", "pending_review"),
        "requires_human_review": True,
        "safety_status": "not_verified",
        "tool_log": tool_log,
    }


