# Rori Marketing

Meta (Facebook/Instagram) paid advertising management for Rori — Belgrade's online pharmacy.

**Part of the [Rori platform](../rori-bible/README.md).** See `AI_CONTEXT.md` for full campaign state.

## What's here

| File | Purpose |
|------|---------|
| `config.py` | All Meta IDs — accounts, audiences, product sets, campaigns, influencer partners |
| `AI_CONTEXT.md` | Full AI context — strategy, IDs, repo structure, token renewal, rules |
| `MARKETING_LOG.md` | Chronological log of every marketing action and decision |
| `src/campaigns.py` | Campaign/ad set/ad CRUD — create, pause, activate, inspect |
| `src/audiences.py` | Custom audience builder — engagement, video viewers, lookalikes |
| `src/partnerships.py` | Partnership ads — fetch eligible influencer content, create branded content ads |
| `src/daily_report.py` | Daily Slack report — campaign metrics, ad breakdown, pixel events |
| `src/meta_api.py` | Low-level Meta Graph API helpers |

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add META_ACCESS_TOKEN and SLACK_WEBHOOK_URL to .env
```

## Usage

```bash
# Check campaign and ad status
python src/campaigns.py

# List all custom audiences
python src/audiences.py

# Report on eligible influencer content
python src/partnerships.py

# Send daily report to Slack
python src/daily_report.py
```

## Active Campaigns (10€/day total)

| Campaign | Objective | Budget | Strategy |
|----------|-----------|--------|----------|
| Brand Awareness - Belgrade | OUTCOME_AWARENESS | 5€/day | Influencer reels + Rori brand videos (7 ads) |
| Catalog Retarget - Belgrade | OUTCOME_SALES | 5€/day | DPA for video viewers + IG/FB engagers (175 products) |

## Automated Reports

Daily Slack report runs at 08:00 CET via GitHub Actions (`.github/workflows/daily-report.yml`).

## GitHub Secrets

| Secret | Description |
|--------|-------------|
| `META_ACCESS_TOKEN` | Long-lived user token (renew every 60 days) |
| `META_APP_SECRET` | App secret for token exchange |
| `META_PAGE_TOKEN` | Long-lived page token |
| `META_PAGE_ID` | Facebook Page ID |
| `META_AD_ACCOUNT_ID` | Ad account (act_...) |
| `META_BUSINESS_ID` | Business Manager ID |
| `META_IG_ACCOUNT_ID` | Instagram Business Account ID |
| `SLACK_WEBHOOK_URL` | Incoming webhook for daily reports |

## Related repos

- **[rori-web-app](https://github.com/karinrori/rori-web-app)** — Pixel events (ViewContent, AddToCart, Purchase) fire from here
- **[rori-bible](https://github.com/karinrori/rori-bible)** — Central Rori documentation and AI context
