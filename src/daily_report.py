"""Daily Slack report for Rori Meta ad campaigns."""

import os
import json
from datetime import datetime, timedelta, timezone
import requests
from dotenv import load_dotenv

load_dotenv()

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GRAPH_API_BASE = "https://graph.facebook.com/v21.0"
AD_ACCOUNT_ID = "act_451952937265646"

CAMPAIGN_IDS = {
    "awareness": "120242237693510751",
    "catalog": "120242237739870751",
}


def meta_get(endpoint: str, params: dict | None = None) -> dict:
    p = {"access_token": META_ACCESS_TOKEN}
    if params:
        p.update(params)
    resp = requests.get(f"{GRAPH_API_BASE}/{endpoint}", params=p, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_campaign_insights(campaign_id: str) -> dict | None:
    data = meta_get(
        f"{campaign_id}/insights",
        {
            "fields": "campaign_name,impressions,reach,clicks,spend,cpc,cpm,ctr,"
            "actions,cost_per_action_type,video_thruplay_watched_actions,"
            "cost_per_thruplay",
            "date_preset": "yesterday",
        },
    )
    return data["data"][0] if data.get("data") else None


def get_ad_insights(campaign_id: str) -> list:
    data = meta_get(
        f"{campaign_id}/insights",
        {
            "fields": "ad_name,impressions,reach,clicks,spend,ctr,actions,"
            "video_thruplay_watched_actions,cost_per_thruplay",
            "date_preset": "yesterday",
            "level": "ad",
            "limit": "20",
        },
    )
    return data.get("data", [])


def get_pixel_stats() -> dict:
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    data = meta_get(
        "555063416919437/stats",
        {"start": yesterday, "end": yesterday},
    )
    events = {}
    for bucket in data.get("data", []):
        for ev in bucket.get("data", []):
            events[ev["value"]] = events.get(ev["value"], 0) + ev["count"]
    return events


def extract_action(actions: list | None, action_type: str) -> str:
    if not actions:
        return "0"
    for a in actions:
        if a.get("action_type") == action_type:
            return a.get("value", "0")
    return "0"


def fmt(val: str | None, prefix: str = "", suffix: str = "") -> str:
    if val is None or val == "0":
        return "-"
    return f"{prefix}{val}{suffix}"


def build_slack_message() -> dict:
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%d.%m.%Y")
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"📊 Rori Daily Ad Report — {yesterday}"},
        },
    ]

    total_spend = 0.0

    for key, cid in CAMPAIGN_IDS.items():
        insights = get_campaign_insights(cid)
        if not insights:
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{key.title()} Campaign*\n_No data yesterday_"},
            })
            continue

        spend = float(insights.get("spend", 0))
        total_spend += spend
        impressions = insights.get("impressions", "0")
        reach = insights.get("reach", "0")
        clicks = insights.get("clicks", "0")
        ctr = insights.get("ctr", "0")
        cpm = insights.get("cpm", "0")
        cpc = insights.get("cpc", "0")

        thruplays = extract_action(
            insights.get("video_thruplay_watched_actions"), "video_view"
        )
        cost_per_thruplay = insights.get("cost_per_thruplay", [{}])
        cpt = cost_per_thruplay[0].get("value", "-") if cost_per_thruplay else "-"

        link_clicks = extract_action(insights.get("actions"), "link_click")
        purchases = extract_action(insights.get("actions"), "offsite_conversion.fb_pixel_purchase")
        add_to_carts = extract_action(insights.get("actions"), "offsite_conversion.fb_pixel_add_to_cart")

        if key == "awareness":
            emoji = "📢"
            name = "Brand Awareness"
            lines = [
                f"*{emoji} {name}*",
                f"💰 Spend: *€{spend:.2f}*  |  👁️ Impressions: *{impressions}*  |  👤 Reach: *{reach}*",
                f"🎬 ThruPlays: *{thruplays}*  |  💵 Cost/ThruPlay: *€{cpt}*",
                f"🖱️ Clicks: *{clicks}*  |  📈 CTR: *{float(ctr):.2f}%*  |  CPM: *€{float(cpm):.2f}*",
            ]
        else:
            emoji = "🛒"
            name = "Catalog Retarget"
            lines = [
                f"*{emoji} {name}*",
                f"💰 Spend: *€{spend:.2f}*  |  👁️ Impressions: *{impressions}*  |  👤 Reach: *{reach}*",
                f"🖱️ Link Clicks: *{link_clicks}*  |  📈 CTR: *{float(ctr):.2f}%*  |  CPC: *€{fmt(cpc)}*",
                f"🛒 Add to Cart: *{add_to_carts}*  |  💳 Purchases: *{purchases}*",
            ]

        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "\n".join(lines)},
        })

        ads = get_ad_insights(cid)
        if ads:
            ad_lines = ["_Top ads:_"]
            for ad in sorted(ads, key=lambda a: float(a.get("spend", 0)), reverse=True)[:5]:
                ad_name = ad.get("ad_name", "?")
                ad_spend = float(ad.get("spend", 0))
                ad_reach = ad.get("reach", "0")
                ad_clicks = ad.get("clicks", "0")
                ad_lines.append(f"  • {ad_name}: €{ad_spend:.2f} | reach {ad_reach} | clicks {ad_clicks}")
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": "\n".join(ad_lines)},
            })

        blocks.append({"type": "divider"})

    pixel_events = get_pixel_stats()
    if pixel_events:
        pv = pixel_events.get("PageView", 0)
        vc = pixel_events.get("ViewContent", 0)
        atc = pixel_events.get("AddToCart", 0)
        ic = pixel_events.get("InitiateCheckout", 0)
        pur = pixel_events.get("Purchase", 0)
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*🔎 Pixel Events (yesterday)*\n"
                    f"PageView: *{pv}* | ViewContent: *{vc}* | "
                    f"AddToCart: *{atc}* | InitiateCheckout: *{ic}* | Purchase: *{pur}*"
                ),
            },
        })

    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"Total spend: *€{total_spend:.2f}* / €10.00 daily budget • Generated at {datetime.now(timezone.utc).strftime('%H:%M UTC')}",
            }
        ],
    })

    return {"blocks": blocks}


def send_to_slack(message: dict) -> None:
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL not set")
    resp = requests.post(
        SLACK_WEBHOOK_URL,
        json=message,
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Slack error {resp.status_code}: {resp.text}")
    print("Slack report sent successfully.")


if __name__ == "__main__":
    msg = build_slack_message()
    print(json.dumps(msg, indent=2, ensure_ascii=False))
    send_to_slack(msg)
