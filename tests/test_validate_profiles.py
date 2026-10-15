import unittest

from src.validate_profiles import validate_market_profile


class TestValidateProfiles(unittest.TestCase):
    def test_empty_profile_is_rejected(self):
        errors = validate_market_profile({})
        self.assertTrue(errors)

    def test_incomplete_draft_is_rejected(self):
        profile = {
            "market_id": "example",
            "country_name": "Example",
            "status": "draft",
            "languages": [],
            "text_direction": "unknown",
            "formatting": {},
            "brand_rules": [],
            "cultural_guidance": [],
            "advertising_rules": [],
            "sources": [],
            "human_review_required": True,
        }

        errors = validate_market_profile(profile)
        self.assertTrue(any("languages" in error for error in errors))
        self.assertTrue(any("text_direction" in error for error in errors))

    def test_valid_draft_passes(self):
        profile = {
            "market_id": "example",
            "country_name": "Example",
            "status": "draft",
            "languages": ["en"],
            "text_direction": "ltr",
            "formatting": {},
            "brand_rules": [],
            "cultural_guidance": [],
            "advertising_rules": [],
            "sources": [],
            "human_review_required": True,
        }

        self.assertEqual(validate_market_profile(profile), [])


if __name__ == "__main__":
    unittest.main()
