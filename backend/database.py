"""Small SQLite persistence layer for the FoodLoop AI prototype."""
import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "foodloop.db"


def get_connection() -> sqlite3.Connection:
    """Return a connection with rows accessible by column name."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    """Create prototype tables if they do not exist."""
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            quantity_kg REAL NOT NULL CHECK(quantity_kg > 0),
            food_category TEXT NOT NULL,
            location TEXT NOT NULL,
            prepared_at TEXT NOT NULL,
            pickup_deadline TEXT NOT NULL,
            storage_notes TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending_review',
            requires_human_review INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organisation_name TEXT NOT NULL,
            food_categories TEXT NOT NULL,
            capacity_kg REAL NOT NULL CHECK(capacity_kg > 0),
            location TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS agent_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER,
            action TEXT NOT NULL,
            rationale TEXT NOT NULL,
            tool_log TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(donation_id) REFERENCES donations(id)
        );
        """)


def create_donation(data: dict[str, Any]) -> dict[str, Any]:
    """Persist a donation, initially requiring human review."""
    with get_connection() as conn:
        cursor = conn.execute("""
        INSERT INTO donations
        (food_name, quantity_kg, food_category, location, prepared_at,
         pickup_deadline, storage_notes, status, requires_human_review)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending_review', 1)
        """, (data["food_name"], data["quantity_kg"], data["food_category"],
              data["location"], data["prepared_at"], data["pickup_deadline"],
              data["storage_notes"]))
        return dict(conn.execute("SELECT * FROM donations WHERE id = ?",
                                 (cursor.lastrowid,)).fetchone())


def list_donations() -> list[dict[str, Any]]:
    """Return donations newest first."""
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM donations ORDER BY id DESC")]


def create_recipient(data: dict[str, Any]) -> dict[str, Any]:
    """Persist a recipient organisation."""
    with get_connection() as conn:
        cursor = conn.execute("""
        INSERT INTO recipients
        (organisation_name, food_categories, capacity_kg, location, contact_name)
        VALUES (?, ?, ?, ?, ?)
        """, (data["organisation_name"], json.dumps(data["food_categories"]),
              data["capacity_kg"], data["location"], data["contact_name"]))
        result = dict(conn.execute("SELECT * FROM recipients WHERE id = ?",
                                   (cursor.lastrowid,)).fetchone())
        result["food_categories"] = json.loads(result["food_categories"])
        return result


def list_recipients() -> list[dict[str, Any]]:
    """Return active recipients and decode food categories."""
    with get_connection() as conn:
        rows = conn.execute(
    "SELECT * FROM recipients WHERE active = 1 ORDER BY id DESC"
).fetchall()
        results = []
        for row in rows:
            item = dict(row)
            item["food_categories"] = json.loads(item["food_categories"])
            results.append(item)
        return results


def log_agent_run(donation_id: int | None, action: str, rationale: str,
                  tool_log: list[dict[str, Any]]) -> None:
    """Persist decision rationale and tool-call summaries for auditability."""
    with get_connection() as conn:
        conn.execute("INSERT INTO agent_runs (donation_id, action, rationale, tool_log) VALUES (?, ?, ?, ?)",
                     (donation_id, action, rationale, json.dumps(tool_log)))


def list_agent_runs() -> list[dict[str, Any]]:
    """Return decision logs newest first."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM agent_runs ORDER BY id DESC").fetchall()
        results = []
        for row in rows:
            item = dict(row)
            item["tool_log"] = json.loads(item["tool_log"])
            results.append(item)
        return results

ALLOWED_STATUSES = {
    "pending_review",
    "match_proposed",
    "accepted",
    "completed",
    "cancelled",
}


def update_donation_status(
    donation_id: int,
    new_status: str,
) -> dict[str, Any] | None:
    """Update a donation status while enforcing allowed transitions."""
    if new_status not in ALLOWED_STATUSES:
        raise ValueError(
            f"Invalid status. Allowed statuses: {sorted(ALLOWED_STATUSES)}"
        )

    allowed_transitions = {
        "pending_review": {"match_proposed", "cancelled"},
        "match_proposed": {"accepted", "pending_review", "cancelled"},
        "accepted": {"completed", "cancelled"},
        "completed": set(),
        "cancelled": set(),
    }

    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM donations WHERE id = ?",
            (donation_id,),
        ).fetchone()

        if row is None:
            return None

        current_status = row["status"]

        if new_status == current_status:
            return dict(row)

        if new_status not in allowed_transitions.get(current_status, set()):
            raise ValueError(
                f"Cannot transition donation from "
                f"'{current_status}' to '{new_status}'."
            )

        conn.execute(
            "UPDATE donations SET status = ? WHERE id = ?",
            (new_status, donation_id),
        )

        updated = conn.execute(
            "SELECT * FROM donations WHERE id = ?",
            (donation_id,),
        ).fetchone()

        return dict(updated)

ALLOWED_STATUSES = {
    "pending_review",
    "match_proposed",
    "accepted",
    "completed",
    "cancelled",
}

ALLOWED_TRANSITIONS = {
    "pending_review": {"match_proposed", "cancelled"},
    "match_proposed": {"accepted", "pending_review", "cancelled"},
    "accepted": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}


def update_donation_status(
    donation_id: int,
    new_status: str,
) -> dict[str, Any] | None:
    """Update a donation status only when the transition is allowed."""

    if new_status not in ALLOWED_STATUSES:
        raise ValueError(
            f"Invalid status. Allowed statuses: {sorted(ALLOWED_STATUSES)}"
        )

    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM donations WHERE id = ?",
            (donation_id,),
        ).fetchone()

        if row is None:
            return None

        current_status = row["status"]

        if new_status == current_status:
            return dict(row)

        if new_status not in ALLOWED_TRANSITIONS.get(current_status, set()):
            raise ValueError(
                f"Cannot change status from '{current_status}' "
                f"to '{new_status}'."
            )

        conn.execute(
            "UPDATE donations SET status = ? WHERE id = ?",
            (new_status, donation_id),
        )

        updated_row = conn.execute(
            "SELECT * FROM donations WHERE id = ?",
            (donation_id,),
        ).fetchone()

        return dict(updated_row)
