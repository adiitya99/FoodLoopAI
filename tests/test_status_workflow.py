import pytest

from backend import database


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    test_path = tmp_path / "foodloop_test.db"
    monkeypatch.setattr(database, "DB_PATH", test_path)
    database.init_db()

    donation = database.create_donation({
        "food_name": "Test Rice",
        "quantity_kg": 5.0,
        "food_category": "prepared_meal",
        "location": "Test Location",
        "prepared_at": "2026-10-21T10:00:00",
        "pickup_deadline": "2026-10-21T14:00:00",
        "storage_notes": "Test storage notes",
    })

    return donation


def test_pending_review_can_be_proposed(test_db):
    updated = database.update_donation_status(
        test_db["id"], "match_proposed"
    )

    assert updated["status"] == "match_proposed"


def test_match_proposed_can_be_accepted(test_db):
    donation_id = test_db["id"]

    database.update_donation_status(donation_id, "match_proposed")
    updated = database.update_donation_status(donation_id, "accepted")

    assert updated["status"] == "accepted"


def test_pending_review_cannot_skip_to_completed(test_db):
    with pytest.raises(ValueError):
        database.update_donation_status(test_db["id"], "completed")


def test_unknown_donation_returns_none(test_db):
    result = database.update_donation_status(999999, "match_proposed")

    assert result is None
