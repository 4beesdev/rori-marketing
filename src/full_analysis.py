"""Full campaign analysis — pulls all key metrics for review."""

import os
import json
from datetime import datetime, timedelta, timezone
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("META_ACCESS_TOKEN")
BASE = "https://graph.facebook.com/v21.0"
AD_ACCOUNT = "act_451952937265646"

CAMPAIGN_IDS = {
    "awareness": "120242237693510751",
    "catalog_retarget": "120242237739870751",
}


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


def analyze():
    # 1. Account overview
    section("ACCOUNT OVERVIEW")
    acc = api(AD_ACCOUNT, {"fields": "name,account_status,currency,balance,amount_spent"})
    print(json.dumps(acc, indent=2))

    # 2. All campaigns status
    section("ALL CAMPAIGNS STATUS")
    camps = api(f"{AD_ACCOUNT}/campaigns", {
        "fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,start_time,budget_remaining",
        "limit": "50",
    })
    for c in camps.get("data", []):
        print(json.dumps(c, indent=2))

    # 3. Per-campaign insights — last 7 days
    for key, cid in CAMPAIGN_IDS.items():
        section(f"CAMPAIGN: {key.upper()} — LAST 7 DAYS")
        try:
            insights = api(f"{cid}/insights", {
                "fields": "campaign_name,impressions,reach,clicks,spend,cpc,cpm,ctr,"
                          "frequency,actions,cost_per_action_type,"
                          "video_thruplay_watched_actions,cost_per_thruplay",
                "date_preset": "last_7d",
            })
            for row in insights.get("data", []):
                print(json.dumps(row, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")

        # Daily breakdown
        section(f"CAMPAIGN: {key.upper()} — DAILY BREAKDOWN (7d)")
        try:
            daily = api(f"{cid}/insights", {
                "fields": "impressions,reach,clicks,spend,ctr,cpm,actions",
                "date_preset": "last_7d",
                "time_increment": "1",
            })
            for row in daily.get("data", []):
                print(json.dumps(row, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")

        # Ad-level breakdown
        section(f"CAMPAIGN: {key.upper()} — AD LEVEL (7d)")
        try:
            ads = api(f"{cid}/insights", {
                "fields": "ad_name,ad_id,impressions,reach,clicks,spend,ctr,cpc,"
                          "actions,video_thruplay_watched_actions,cost_per_thruplay",
                "date_preset": "last_7d",
                "level": "ad",
                "limit": "30",
            })
            for row in ads.get("data", []):
                print(json.dumps(row, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")

    # 4. Last 30 days overview
    section("LAST 30 DAYS — ACCOUNT LEVEL")
    try:
        monthly = api(f"{AD_ACCOUNT}/insights", {
            "fields": "impressions,reach,clicks,spend,cpc,cpm,ctr,frequency,"
                      "actions,cost_per_action_type",
            "date_preset": "last_30d",
        })
        for row in monthly.get("data", []):
            print(json.dumps(row, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

    # 5. Age & gender breakdown (30d)
    section("DEMOGRAPHICS — AGE & GENDER (30d)")
    try:
        demo = api(f"{AD_ACCOUNT}/insights", {
            "fields": "impressions,reach,clicks,spend,ctr",
            "date_preset": "last_30d",
            "breakdowns": "age,gender",
        })
        for row in demo.get("data", []):
            print(json.dumps(row, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

    # 6. Placement breakdown (30d)
    section("PLACEMENTS (30d)")
    try:
        place = api(f"{AD_ACCOUNT}/insights", {
            "fields": "impressions,reach,clicks,spend,ctr,cpm",
            "date_preset": "last_30d",
            "breakdowns": "publisher_platform,platform_position",
        })
        for row in place.get("data", []):
            print(json.dumps(row, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

    # 7. Pixel events
    section("PIXEL EVENTS (last 7 days)")
    for i in range(7):
        day = (datetime.now(timezone.utc) - timedelta(days=i + 1)).strftime("%Y-%m-%d")
        try:
            px = api("555063416919437/stats", {"start": day, "end": day})
            events = {}
            for bucket in px.get("data", []):
                for ev in bucket.get("data", []):
                    events[ev["value"]] = events.get(ev["value"], 0) + ev["count"]
            if events:
                print(f"{day}: {json.dumps(events)}")
        except Exception as e:
            print(f"{day}: Error — {e}")

    print("\n\nDONE.")


if __name__ == "__main__":
    analyze()
