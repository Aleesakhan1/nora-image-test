
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.market_profiles import (
    list_market_profiles,
    load_market_profile,
)


class TestMarketProfiles(unittest.TestCase):
    def test_profile_listing_returns_a_list(self):
        profiles = list_market_profiles()
        self.assertIsInstance(profiles, list)

    def test_template_is_not_listed_as_a_country(self):
        profiles = list_market_profiles()
        self.assertNotIn("template", profiles)

    def make_profile(self, status="approved", sources=None):
        return {
            "market_id": "example",
            "country_name": "Example Country",
            "status": status,
            "languages": ["en"],
            "text_direction": "ltr",
            "formatting": {},
            "brand_rules": [],
            "cultural_guidance": [],
            "advertising_rules": [],
            "sources": sources if sources is not None else [
                {
                    "title": "Official example source",
                    "url": "https://example.com",
                }
            ],
            "human_review_required": True,
        }

    def load_test_profile(self, profile):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "example.json"
            profile_path.write_text(
                json.dumps(profile),
                encoding="utf-8",
            )

            with patch(
                "src.market_profiles.PROFILES_DIR",
                Path(directory),
            ):
                return load_market_profile("example")

    def test_draft_profile_is_rejected(self):
        profile = self.make_profile(status="draft")

        with self.assertRaisesRegex(ValueError, "not approved"):
            self.load_test_profile(profile)

    def test_approved_profile_without_sources_is_rejected(self):
        profile = self.make_profile(sources=[])

        with self.assertRaisesRegex(ValueError, "sources"):
            self.load_test_profile(profile)

    def test_valid_approved_profile_loads(self):
        profile = self.make_profile()

        loaded = self.load_test_profile(profile)

        self.assertEqual(loaded["market_id"], "example")
        self.assertEqual(loaded["status"], "approved")


if __name__ == "__main__":
    unittest.main()