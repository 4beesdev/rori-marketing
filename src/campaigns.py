"""Campaign management — create, pause, activate, and inspect campaigns."""

import os
import sys
import json
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import (
    AD_ACCOUNT_ID, PAGE_ID, IG_ACCOUNT_ID, GRAPH_API_BASE,
    CAMPAIGNS, PAUSED_CAMPAIGNS,
)

load_dotenv()
TOKEN = os.getenv("META_ACCESS_TOKEN")


def api(method: str, endpoint: str, **kwargs) -> dict:
    url = f"{GRAPH_API_BASE}/{endpoint}"
    kwargs.setdefault("params" if method == "GET" else "data", {})["access_token"] = TOKEN
    resp = getattr(requests, method.lower())(url, timeout=30, **kwargs)
    resp.raise_for_status()
    return resp.json()


def create_campaign(name: str, objective: str, status: str = "PAUSED", promoted_object: dict | None = None) -> str:
    payload = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": "[]",
    }
    if promoted_object:
        payload["promoted_object"] = json.dumps(promoted_object)
    result = api("POST", f"{AD_ACCOUNT_ID}/campaigns", data=payload)
    print(f"Campaign created: {result['id']} — {name}")
    return result["id"]


def create_adset(
    campaign_id: str,
    name: str,
    daily_budget: int,
    optimization_goal: str,
    targeting: dict,
    promoted_object: dict | None = None,
    status: str = "PAUSED",
) -> str:
    payload = {
        "campaign_id": campaign_id,
        "name": name,
        "daily_budget": str(daily_budget),
        "billing_event": "IMPRESSIONS",
        "optimization_goal": optimization_goal,
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "status": status,
        "targeting": json.dumps(targeting),
    }
    if promoted_object:
        payload["promoted_object"] = json.dumps(promoted_object)
    result = api("POST", f"{AD_ACCOUNT_ID}/adsets", data=payload)
    print(f"Ad set created: {result['id']} — {name}")
    return result["id"]


def create_video_ad(
    adset_id: str,
    name: str,
    video_id: str,
    message: str,
    link: str,
    thumbnail_url: str,
    status: str = "PAUSED",
) -> str:
    creative = {
        "object_story_spec": {
            "page_id": PAGE_ID,
            "video_data": {
                "video_id": video_id,
                "image_url": thumbnail_url,
                "message": message,
                "call_to_action": {"type": "LEARN_MORE", "value": {"link": link}},
            },
        }
    }
    result = api("POST", f"{AD_ACCOUNT_ID}/ads", data={
        "adset_id": adset_id,
        "name": name,
        "status": status,
        "creative": json.dumps(creative),
    })
    print(f"Video ad created: {result['id']} — {name}")
    return result["id"]


def create_dpa_ad(adset_id: str, name: str, product_set_id: str, status: str = "PAUSED") -> str:
    creative = {
        "object_story_spec": {
            "page_id": PAGE_ID,
            "template_data": {
                "message": "{{product.name}} – sada dostupno na Rori.app 🛒",
                "link": "https://rori.app",
                "name": "{{product.name}}",
                "description": "{{product.current_price}}",
                "call_to_action": {"type": "SHOP_NOW"},
            },
        },
        "product_set_id": product_set_id,
    }
    result = api("POST", f"{AD_ACCOUNT_ID}/ads", data={
        "adset_id": adset_id,
        "name": name,
        "status": status,
        "creative": json.dumps(creative),
    })
    print(f"DPA ad created: {result['id']} — {name}")
    return result["id"]


def set_status(object_id: str, status: str) -> bool:
    result = api("POST", object_id, data={"status": status})
    ok = result.get("success", False)
    print(f"{'✓' if ok else '✗'} {object_id} → {status}")
    return ok


def pause_campaign(campaign_id: str) -> bool:
    return set_status(campaign_id, "PAUSED")


def activate_campaign(campaign_id: str) -> bool:
    return set_status(campaign_id, "ACTIVE")


def get_campaign_status() -> None:
    data = api("GET", f"{AD_ACCOUNT_ID}/campaigns", params={
        "fields": "id,name,status,effective_status,objective,daily_budget",
        "limit": "20",
    })
    print(f"\n{'Status':<20} {'Objective':<25} Name")
    print("-" * 75)
    for c in data.get("data", []):
        print(f"{c.get('effective_status','?'):<20} {c.get('objective','?'):<25} {c['name']}")


def get_ad_status(adset_id: str) -> None:
    data = api("GET", f"{adset_id}/ads", params={"fields": "id,name,effective_status"})
    for ad in data.get("data", []):
        print(f"  {ad.get('effective_status','?'):<20} {ad['name']}")


if __name__ == "__main__":
    get_campaign_status()
    for key, camp in CAMPAIGNS.items():
        print(f"\n--- {camp['name']} ads ---")
        get_ad_status(camp["adset_id"])
