"""Partnership Ads — fetch eligible influencer content and create branded content ads."""

import os
import sys
import json
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import (
    AD_ACCOUNT_ID, PAGE_ID, IG_ACCOUNT_ID, GRAPH_API_BASE,
    INFLUENCER_PARTNERS,
)

load_dotenv()
TOKEN = os.getenv("META_ACCESS_TOKEN")


def api(method: str, endpoint: str, **kwargs) -> dict:
    url = f"{GRAPH_API_BASE}/{endpoint}"
    kwargs.setdefault("params" if method == "GET" else "data", {})["access_token"] = TOKEN
    resp = getattr(requests, method.lower())(url, timeout=30, **kwargs)
    resp.raise_for_status()
    return resp.json()


def fetch_eligible_media(creator_username: str | None = None) -> list[dict]:
    """Fetch all branded content media eligible for partnership ads."""
    params = {
        "fields": "id,permalink,owner_id,eligibility_errors,has_permission_for_partnership_ad",
        "limit": "50",
    }
    if creator_username:
        params["creator_username"] = creator_username
    data = api("GET", f"{IG_ACCOUNT_ID}/branded_content_advertisable_medias", params=params)
    return data.get("data", [])


def fetch_tagged_media() -> list[dict]:
    """Fetch all IG posts where Rori is tagged."""
    data = api("GET", f"{IG_ACCOUNT_ID}/tags", params={
        "fields": "id,caption,timestamp,media_type,permalink,username",
        "limit": "50",
    })
    return data.get("data", [])


def create_partnership_creative(source_media_id: str, name: str) -> str:
    """Create an ad creative from an influencer's IG post."""
    result = api("POST", f"{AD_ACCOUNT_ID}/adcreatives", data={
        "name": name,
        "object_id": PAGE_ID,
        "source_instagram_media_id": source_media_id,
        "facebook_branded_content": json.dumps({"sponsor_page_id": PAGE_ID}),
        "instagram_branded_content": json.dumps({"sponsor_id": IG_ACCOUNT_ID}),
        "branded_content": json.dumps({"ad_format": "1"}),
    })
    print(f"Creative created: {result['id']} — {name}")
    return result["id"]


def create_partnership_ad(adset_id: str, creative_id: str, name: str, status: str = "ACTIVE") -> str:
    """Create a partnership ad from an existing creative."""
    result = api("POST", f"{AD_ACCOUNT_ID}/ads", data={
        "adset_id": adset_id,
        "name": name,
        "status": status,
        "creative": json.dumps({"creative_id": creative_id}),
    })
    print(f"Partnership ad created: {result['id']} — {name}")
    return result["id"]


def upload_ig_video_to_fb(source_media_id: str) -> str:
    """Upload an IG video to Facebook ad library (needed for some creator videos)."""
    result = api("POST", f"{AD_ACCOUNT_ID}/advideos", data={
        "source_instagram_media_id": source_media_id,
        "is_partnership_ad": "true",
    })
    print(f"Video uploaded: {result['id']}")
    return result["id"]


def report_eligible_content() -> None:
    """Print a report of all eligible branded content."""
    media = fetch_eligible_media()
    eligible = [m for m in media if not m.get("eligibility_errors") and m.get("has_permission_for_partnership_ad")]
    blocked = [m for m in media if m.get("eligibility_errors")]
    no_perm = [m for m in media if not m.get("has_permission_for_partnership_ad") and not m.get("eligibility_errors")]

    print(f"\n=== Branded Content Report ===")
    print(f"Total: {len(media)} | Eligible: {len(eligible)} | Blocked: {len(blocked)} | No Permission: {len(no_perm)}")

    owner_map = {v["ig_id"]: k for k, v in INFLUENCER_PARTNERS.items()}

    print(f"\n✅ Eligible ({len(eligible)}):")
    for m in eligible:
        owner = owner_map.get(m["owner_id"], m["owner_id"])
        print(f"  {m['id']} | @{owner} | {m['permalink']}")

    if blocked:
        print(f"\n❌ Blocked ({len(blocked)}):")
        for m in blocked:
            owner = owner_map.get(m["owner_id"], m["owner_id"])
            errors = "; ".join(m.get("eligibility_errors", []))
            print(f"  {m['id']} | @{owner} | {errors}")

    if no_perm:
        print(f"\n⏳ No Permission ({len(no_perm)}):")
        for m in no_perm:
            owner = owner_map.get(m["owner_id"], m["owner_id"])
            print(f"  {m['id']} | @{owner} | {m['permalink']}")


if __name__ == "__main__":
    report_eligible_content()
