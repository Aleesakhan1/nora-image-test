from typing import Any


REQUIRED_FIELDS = [
    "market_id",
    "country_name",
    "status",
    "languages",
    "text_direction",
    "formatting",
    "brand_rules",
    "cultural_guidance",
    "advertising_rules",
    "sources",
    "human_review_required",
]

VALID_TEXT_DIRECTIONS = {"ltr", "rtl", "mixed"}


def validate_market_profile(profile: dict[str, Any]) -> list[str]:
    """Return validation errors for a market profile."""
    errors = []

    if not isinstance(profile, dict):
        return ["Profile must be a JSON object."]

    for field in REQUIRED_FIELDS:
        if field not in profile:
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    if not isinstance(profile["market_id"], str) or not profile["market_id"].strip():
        errors.append("market_id must be a non-empty string.")

    if not isinstance(profile["country_name"], str) or not profile["country_name"].strip():
        errors.append("country_name must be a non-empty string.")

    if profile["status"] not in {"draft", "review", "approved"}:
        errors.append("status must be draft, review, or approved.")

    if not isinstance(profile["languages"], list) or not profile["languages"]:
        errors.append("languages must be a non-empty list.")

    if profile["text_direction"] not in VALID_TEXT_DIRECTIONS:
        errors.append("text_direction must be ltr, rtl, or mixed.")

    for field in ("formatting",):
        if not isinstance(profile[field], dict):
            errors.append(f"{field} must be an object.")

    for field in ("brand_rules", "cultural_guidance", "advertising_rules", "sources"):
        if not isinstance(profile[field], list):
            errors.append(f"{field} must be a list.")

    if not isinstance(profile["human_review_required"], bool):
        errors.append("human_review_required must be true or false.")

    if profile["status"] == "approved" and not profile["sources"]:
        errors.append("Approved profiles must include sources.")

    return errors
