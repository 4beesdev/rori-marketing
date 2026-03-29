"""Full campaign analysis — pulls metrics only for ACTIVE campaigns, adsets and ads."""

import os
import json
from datetime import datetime, timedelta, timezone
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("META_ACCESS_TOKEN")
BASE = "https://graph.facebook.com/v21.0"
AD_ACCOUNT = "act_451952937265646"
PIXEL_ID = "555063416919437"

CAMPAIGN_IDS = {
    "awareness": "120242237693510751",
    "catalog_retarget": "120242237739870751",
}

# Campaign start date — used for "since launch" queries
LAUNCH_DATE = "2026-03-19"


def api(endpoint, params=None):
    p = {"access_token": TOKEN}
    if params:
        p.update(params)
    resp = requests.get(f"{BASE}/{endpoint}", params=p, timeout=30)
    resp.raise_for_status()
    return resp.json()


def section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def time_range_since_launch():
    return json.dumps({"since": LAUNCH_DATE, "until": today_str()})


def analyze():
    # 1. Account overview
    section("ACCOUNT OVERVIEW")
    acc = api(AD_ACCOUNT, {"fields": "name,account_status,currency,balance,amount_spent"})
    print(json.dumps(acc, indent=2))

    # 2. Active campaigns only
    section("ACTIVE CAMPAIGNS")
    camps = api(f"{AD_ACCOUNT}/campaigns", {
        "fields": "id,name,status,effective_status,objective,daily_budget,start_time,budget_remaining",
        "filtering": json.dumps([{"field": "effective_status", "operator": "IN", "value": ["ACTIVE"]}]),
        "limit": "50",
    })
    for c in camps.get("data", []):
        print(json.dumps(c, indent=2))

    # 3. Per-campaign insights (since launch, only active adsets/ads)
    for key, cid in CAMPAIGN_IDS.items():
        section(f"CAMPAIGN: {key.upper()} — SINCE LAUNCH ({LAUNCH_DATE})")
        try:
            insights = api(f"{cid}/insights", {
                "fields": "campaign_name,impressions,reach,clicks,spend,cpc,cpm,ctr,"
                          "frequency,actions,cost_per_action_type,"
                          "video_thruplay_watched_actions,cost_per_thruplay",
                "time_range": time_range_since_launch(),
                "filtering": json.dumps([{"field": "ad.effective_status", "operator": "IN", "value": ["ACTIVE"]}]),
            })
            for row in insights.get("data", []):
                print(json.dumps(row, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")

        # Daily breakdown (active ads only)
        section(f"CAMPAIGN: {key.upper()} — DAILY BREAKDOWN (since launch)")
        try:
            daily = api(f"{cid}/insights", {
                "fields": "impressions,reach,clicks,spend,ctr,cpm,actions",
                "time_range": time_range_since_launch(),
                "time_increment": "1",
                "filtering": json.dumps([{"field": "ad.effective_status", "operator": "IN", "value": ["ACTIVE"]}]),
            })
            for row in daily.get("data", []):
                print(json.dumps(row, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")

        # Ad-level breakdown (active ads only)
        section(f"CAMPAIGN: {key.upper()} — ACTIVE ADS (since launch)")
        try:
            ads = api(f"{cid}/insights", {
                "fields": "ad_name,ad_id,impressions,reach,clicks,spend,ctr,cpc,"
                          "actions,video_thruplay_watched_actions,cost_per_thruplay",
                "time_range": time_range_since_launch(),
                "level": "ad",
                "limit": "30",
                "filtering": json.dumps([{"field": "ad.effective_status", "operator": "IN", "value": ["ACTIVE"]}]),
            })
            for row in ads.get("data", []):
                print(json.dumps(row, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")

    # 4. Demographics — active campaigns only (since launch)
    section("DEMOGRAPHICS — AGE & GENDER (active campaigns, since launch)")
    try:
        campaign_filter = json.dumps([
            {"field": "campaign.id", "operator": "IN", "value": list(CAMPAIGN_IDS.values())},
            {"field": "ad.effective_status", "operator": "IN", "value": ["ACTIVE"]},
        ])
        demo = api(f"{AD_ACCOUNT}/insights", {
            "fields": "impressions,reach,clicks,spend,ctr",
            "time_range": time_range_since_launch(),
            "breakdowns": "age,gender",
            "filtering": campaign_filter,
        })
        for row in demo.get("data", []):
            print(json.dumps(row, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

    # 5. Placements — active campaigns only (since launch)
    section("PLACEMENTS (active campaigns, since launch)")
    try:
        place = api(f"{AD_ACCOUNT}/insights", {
            "fields": "impressions,reach,clicks,spend,ctr,cpm",
            "time_range": time_range_since_launch(),
            "breakdowns": "publisher_platform,platform_position",
            "filtering": campaign_filter,
        })
        for row in place.get("data", []):
            print(json.dumps(row, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

    # 6. Pixel events (real daily stats)
    section("PIXEL EVENTS (last 7 days)")
    for i in range(7):
        day = (datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y-%m-%d")
        try:
            px = api(f"{PIXEL_ID}/stats", {
                "aggregation": "event",
                "start_time": day,
                "end_time": day,
            })
            events = {}
            for bucket in px.get("data", []):
                for ev in bucket.get("data", []):
                    events[ev["value"]] = events.get(ev["value"], 0) + ev["count"]
            if events:
                print(f"{day}: {json.dumps(events)}")
            else:
                print(f"{day}: no events")
        except Exception as e:
            print(f"{day}: Error — {e}")

    print("\n\nDONE.")


if __name__ == "__main__":
    analyze()
