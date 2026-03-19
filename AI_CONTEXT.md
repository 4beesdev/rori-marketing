# AI_CONTEXT.md — Rori Marketing

AI context file for the rori-marketing repository. Read this first in any new session.

## What is this repo?

Meta (Facebook/Instagram) paid advertising management for Rori — an online pharmacy/drugstore in Belgrade, Serbia. Campaign creation, audience building, partnership ads, and daily reporting — all managed via Meta Marketing API.

**Parent project**: See `rori-bible/AI_CONTEXT.md` for full platform context.

## Current Strategy

**Funnel** (10€/day, Belgrade, Women 18-45):
1. **TOF — Awareness** (5€/day): Boost influencer reels + Rori brand videos for Vivienne Sabó, Caudalie, and Anastasia Beverly Hills.
2. **MOF — Catalog Retarget** (5€/day): Dynamic Product Ads targeting people who watched videos or engaged with IG/FB page. Shows products from the 3 influencer brands.
3. **Expansion** (future): Lookalike audiences when retarget pool > 1000 people.

## Key IDs

| Resource | ID |
|----------|-----|
| Ad Account | act_451952937265646 |
| Business | 1693182164399002 |
| Facebook Page | 383041474901753 |
| Instagram Account | 17841452496126909 |
| Pixel (active on web) | 555063416919437 |
| Product Catalog | 2543619572695742 |

See `config.py` for complete IDs including audiences, product sets, campaigns, and influencer partners.

## Repo Structure

```
rori-marketing/
├── config.py                  # All Meta IDs, audiences, campaigns, partners
├── AI_CONTEXT.md              # This file — AI context for new sessions
├── MARKETING_LOG.md           # Chronological log of all actions & decisions
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore
├── README.md
├── src/
│   ├── meta_api.py            # Low-level Meta Graph API helpers
│   ├── campaigns.py           # Campaign/adset/ad CRUD operations
│   ├── audiences.py           # Custom audience builder (engagement, video, lookalike)
│   ├── partnerships.py        # Partnership ads (influencer branded content)
│   └── daily_report.py        # Daily Slack report (runs via GitHub Actions)
└── .github/
    └── workflows/
        └── daily-report.yml   # Cron: 07:00 UTC daily → Slack webhook
```

## GitHub Secrets (4beesdev/rori-marketing)

| Secret | Description |
|--------|-------------|
| META_ACCESS_TOKEN | Long-lived user access token (60 days, expires ~May 2026) |
| META_APP_SECRET | 9de52fe40626979a8cff49d6247986a9 |
| META_PAGE_TOKEN | Long-lived page access token |
| META_PAGE_ID | 383041474901753 |
| META_AD_ACCOUNT_ID | act_451952937265646 |
| META_BUSINESS_ID | 1693182164399002 |
| META_IG_ACCOUNT_ID | 17841452496126909 |
| SLACK_WEBHOOK_URL | Slack incoming webhook for daily reports |

## Active Campaigns

### 1. Rori Brand Awareness - Belgrade
- **ID**: 120242237693510751
- **Budget**: 5€/day (500 cents)
- **Objective**: OUTCOME_AWARENESS (ThruPlay optimization)
- **Targeting**: Belgrade city (key 2673746), Women 18-45
- **Ads** (7):
  - 3x Rori video ads (VS, Caudalie, ABH)
  - 4x Partnership ads (@la_reina_dulce, @lady_withhat, @mamma.m.i.a, @viviennesabo.serbia)

### 2. Rori Catalog Retarget - Belgrade
- **ID**: 120242237739870751
- **Budget**: 5€/day (500 cents)
- **Objective**: OUTCOME_SALES (Purchase optimization)
- **Retarget audiences**: All Brands Video Viewers + IG Engagers + Page Engagers
- **Product set**: VS + Caudalie + ABH (175 products)
- **Ad**: Dynamic Product Ad (template creative)

## Pixel Implementation (rori-web-app)

Pixel code lives in `rori-web-app/lib/meta-pixel.ts`. Events:
- `PageView` — auto on every page load (via MetaPixelLoader component)
- `ViewContent` — on product page view and product dialog open
- `AddToCart` — on successful add to cart (requires login + marketing consent)
- `InitiateCheckout` — on checkout button click
- `Purchase` — on order completion (finishOrder success)

All events gated by `hasMarketingConsent()` from cookie consent system.

**Critical**: Pixel `555063416919437` connected to catalog `2543619572695742` (done 2026-03-19). `content_ids` in pixel events match `retailer_id` in catalog.

## Influencer Partners

8 influencer accounts with active/pending branded content partnerships. See `config.py` `INFLUENCER_PARTNERS` for full list. 46 reels eligible for partnership ads.

## Token Expiration

Long-lived tokens expire after 60 days. Current token set: ~2026-03-19. **Renew before ~2026-05-18.**

To renew:
1. Generate new short-lived token in Graph API Explorer with all permissions
2. Exchange for long-lived: `GET /oauth/access_token?grant_type=fb_exchange_token&client_id=616466693826814&client_secret={APP_SECRET}&fb_exchange_token={SHORT_TOKEN}`
3. Update `META_ACCESS_TOKEN` GitHub secret
4. Get new page token: `GET /me/accounts?fields=access_token` → update `META_PAGE_TOKEN`

## What NOT to do

- Don't touch campaigns during learning phase (first 7 days)
- Don't increase daily budget by more than 20% at a time
- Don't create duplicate audiences (check `audiences.py list_audiences()` first)
- Don't modify legacy paused campaigns — they exist for historical reference only
