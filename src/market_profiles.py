
import json
from pathlib import Path

from src.validate_profiles import validate_market_profile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = PROJECT_ROOT / "data" / "market_profiles"


def list_market_profiles():
    """List country profiles, excluding the template."""
    return sorted(
        path.stem
        for path in PROFILES_DIR.glob("*.json")
        if path.stem != "template"
    )


def load_market_profile(market_id):
    """Load and validate an approved country profile."""
    if (
        not isinstance(market_id, str)
        or not market_id
        or Path(market_id).name != market_id
        or market_id in {".", ".."}
    ):
        raise ValueError("Invalid market ID.")

    profile_path = PROFILES_DIR / f"{market_id}.json"

    if not profile_path.is_file():
        raise FileNotFoundError(
            f"No market profile found for '{market_id}'."
        )

    with profile_path.open("r", encoding="utf-8") as file:
        profile = json.load(file)

    if not isinstance(profile, dict):
        raise ValueError("Market profile must be a JSON object.")

    if profile.get("market_id") != market_id:
        raise ValueError("Profile market_id does not match its filename.")

    errors = validate_market_profile(profile)
    if errors:
        raise ValueError("Invalid market profile: " + "; ".join(errors))

    if profile["status"] != "approved":
        raise ValueError(
            f"Market profile '{market_id}' is not approved for production."
        )

    return profile