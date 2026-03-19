"""Audience builder — create and manage custom audiences for retargeting."""

import os
import sys
import json
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import AD_ACCOUNT_ID, PAGE_ID, IG_ACCOUNT_ID, GRAPH_API_BASE, AUDIENCES

load_dotenv()
TOKEN = os.getenv("META_ACCESS_TOKEN")


def api(method: str, endpoint: str, **kwargs) -> dict:
    url = f"{GRAPH_API_BASE}/{endpoint}"
    kwargs.setdefault("params" if method == "GET" else "data", {})["access_token"] = TOKEN
    resp = getattr(requests, method.lower())(url, timeout=30, **kwargs)
    resp.raise_for_status()
    return resp.json()


def create_page_engagement_audience(name: str, event: str, retention_days: int = 30) -> str:
    """Create audience from Facebook Page engagement events.

    Valid events: page_engaged, page_post_interaction, page_visited,
    page_liked, page_cta_clicked, page_messaged, page_or_post_save.
    """
    rule = {
        "inclusions": {
            "operator": "or",
            "rules": [{
                "event_sources": [{"id": PAGE_ID, "type": "page"}],
                "retention_seconds": retention_days * 86400,
                "filter": {
                    "operator": "and",
                    "filters": [{"field": "event", "operator": "eq", "value": event}],
                },
            }],
        }
    }
    result = api("POST", f"{AD_ACCOUNT_ID}/customaudiences", data={
        "name": name,
        "prefill": "1",
        "rule": json.dumps(rule),
    })
    print(f"Page audience created: {result['id']} — {name}")
    return result["id"]


def create_ig_engagement_audience(name: str, event: str = "ig_business_profile_all", retention_days: int = 30) -> str:
    """Create audience from Instagram engagement events.

    Valid events: ig_business_profile_all, ig_business_profile_engaged,
    ig_business_profile_visit, ig_organic_like, ig_organic_comment, etc.
    """
    rule = {
        "inclusions": {
            "operator": "or",
            "rules": [{
                "event_sources": [{"id": IG_ACCOUNT_ID, "type": "ig_business"}],
                "retention_seconds": retention_days * 86400,
                "filter": {
                    "operator": "and",
                    "filters": [{"field": "event", "operator": "eq", "value": event}],
                },
            }],
        }
    }
    result = api("POST", f"{AD_ACCOUNT_ID}/customaudiences", data={
        "name": name,
        "prefill": "1",
        "rule": json.dumps(rule),
    })
    print(f"IG audience created: {result['id']} — {name}")
    return result["id"]


def create_video_viewers_audience(name: str, video_ids: list[str], event: str = "video_view_50_percent") -> str:
    """Create audience from video viewers.

    Valid events: video_watched (3s+), video_view_10s, video_view_15s,
    video_view_25_percent, video_view_50_percent, video_view_75_percent,
    video_completed (95%).
    """
    rule = [{"object_id": vid, "event_name": event} for vid in video_ids]
    result = api("POST", f"{AD_ACCOUNT_ID}/customaudiences", data={
        "name": name,
        "subtype": "ENGAGEMENT",
        "prefill": "1",
        "description": f"Video viewers ({event}) for {len(video_ids)} videos",
        "rule": json.dumps(rule),
    })
    print(f"Video audience created: {result['id']} — {name}")
    return result["id"]


def create_lookalike(source_audience_id: str, name: str, country: str = "RS", ratio: float = 0.01) -> str:
    """Create a lookalike audience from a source custom audience.

    ratio: 0.01 = top 1% (most similar), up to 0.20 = top 20%.
    """
    result = api("POST", f"{AD_ACCOUNT_ID}/customaudiences", data={
        "name": name,
        "subtype": "LOOKALIKE",
        "origin_audience_id": source_audience_id,
        "lookalike_spec": json.dumps({
            "type": "similarity",
            "country": country,
            "ratio": ratio,
        }),
    })
    print(f"Lookalike created: {result['id']} — {name}")
    return result["id"]


def list_audiences() -> None:
    data = api("GET", f"{AD_ACCOUNT_ID}/customaudiences", params={
        "fields": "id,name,subtype,approximate_count,operation_status",
        "limit": "50",
    })
    print(f"\n{'Size':<10} {'Status':<10} Name")
    print("-" * 60)
    for a in data.get("data", []):
        size = a.get("approximate_count", "?")
        status_code = a.get("operation_status", {}).get("code", "?")
        print(f"{str(size):<10} {str(status_code):<10} {a['name']}")


if __name__ == "__main__":
    list_audiences()
