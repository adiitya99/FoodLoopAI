"""Basic smoke tests. Run: python -m unittest discover -s tests"""
import unittest
from backend.main import app
from backend.matching import rank_recipients


class FoodLoopSmokeTests(unittest.TestCase):
    def test_app_title(self):
        self.assertEqual(app.title, "FoodLoop AI")

    def test_matching_filters_category_and_capacity(self):
        donation = {
            "food_category": "bakery",
            "quantity_kg": 5,
            "pickup_deadline": "2026-10-19T14:00:00",
        }
        recipients = [
            {"id": 1, "organisation_name": "Suitable", "food_categories": ["bakery"],
             "capacity_kg": 10, "location": "Kokrajhar"},
            {"id": 2, "organisation_name": "Wrong category", "food_categories": ["produce"],
             "capacity_kg": 10, "location": "Kokrajhar"},
            {"id": 3, "organisation_name": "Too small", "food_categories": ["bakery"],
             "capacity_kg": 2, "location": "Kokrajhar"},
        ]
        results = rank_recipients(donation, recipients)
        self.assertEqual([r["recipient_id"] for r in results], [1])
        self.assertTrue(results[0]["requires_human_review"])


if __name__ == "__main__":
    unittest.main()
