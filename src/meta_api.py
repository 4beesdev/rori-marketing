import os
import requests
from dotenv import load_dotenv

load_dotenv()

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
GRAPH_API_BASE = "https://graph.facebook.com/v21.0"


def get_me():
    """Verify token and get basic account info."""
    resp = requests.get(
        f"{GRAPH_API_BASE}/me",
        params={"access_token": META_ACCESS_TOKEN},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_ad_accounts():
    """List ad accounts the token has access to."""
    resp = requests.get(
        f"{GRAPH_API_BASE}/me/adaccounts",
        params={
            "access_token": META_ACCESS_TOKEN,
            "fields": "id,name,account_status,currency",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_campaigns(ad_account_id: str):
    """Get campaigns for an ad account."""
    resp = requests.get(
        f"{GRAPH_API_BASE}/{ad_account_id}/campaigns",
        params={
            "access_token": META_ACCESS_TOKEN,
            "fields": "id,name,status,objective,daily_budget,lifetime_budget",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_campaign_insights(campaign_id: str, date_preset: str = "last_30d"):
    """Get performance insights for a campaign."""
    resp = requests.get(
        f"{GRAPH_API_BASE}/{campaign_id}/insights",
        params={
            "access_token": META_ACCESS_TOKEN,
            "fields": "impressions,clicks,spend,cpc,cpm,ctr,reach,actions",
            "date_preset": date_preset,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    print("Verifying Meta API connection...")
    try:
        me = get_me()
        print(f"Connected as: {me}")

        accounts = get_ad_accounts()
        print(f"\nAd accounts: {accounts}")

        if accounts.get("data"):
            acc_id = accounts["data"][0]["id"]
            campaigns = get_campaigns(acc_id)
            print(f"\nCampaigns for {acc_id}: {campaigns}")
    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e}")
        print(f"Response: {e.response.text}")
