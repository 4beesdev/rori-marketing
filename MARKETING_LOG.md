# MARKETING_LOG.md — Rori Meta Ads

Chronological log of all marketing actions, decisions, and results.

---

## 2026-03-19 — Initial Campaign Setup

### Analysis
- Analyzed all Meta ad campaigns from 2025-01-01 to present.
- Previous campaigns focused on app installs for all of Serbia with high frequency and no webshop conversion tracking.
- Webshop launched 2026-02-01; catalog has ~3,880 products.
- Decision: start fresh with webshop-focused strategy for Belgrade market.

### Strategy Defined
- **Funnel**: TOF (awareness via influencer reels) → MOF (catalog retarget for engaged users) → Expansion (lookalikes when data sufficient).
- **Budget**: 10€/day total (5€ awareness + 5€ catalog retarget).
- **Target**: Belgrade, Women 18-45.
- **Brands in focus**: Vivienne Sabó, Caudalie, Anastasia Beverly Hills (influencer collaboration brands).

### Token & Permissions
- Obtained long-lived 60-day user access token with 34 permissions including `instagram_branded_content_ads_brand`.
- Obtained long-lived page access token.
- All tokens stored as GitHub secrets in `4beesdev/rori-marketing`.

### Product Sets Created
| Name | ID | Count |
|------|-----|-------|
| Vivienne Sabo | 957383383629326 | 144 |
| Caudalie | 26711159618470309 | 16 |
| Anastasia Beverly Hills | 790185514136659 | 15 |
| VS + Caudalie + ABH (Influencer Brands) | 3854033414900814 | 175 |

### Custom Audiences Created (6)
| Name | ID | Type |
|------|-----|------|
| Rori IG Engagers 30d | 120242237614610751 | IG engagement |
| Rori Page Engagers 30d | 120242237616080751 | Page engagement |
| VS Video Viewers 50% | 120242237649310751 | Video (3 videos) |
| Caudalie Video Viewers 50% | 120242237651680751 | Video (4 videos) |
| ABH Video Viewers 50% | 120242237654210751 | Video (1 video) |
| All Brands Video Viewers 50% | 120242237655790751 | Video (8 videos) |

### Campaigns Created & Activated

**Campaign 1: Rori Brand Awareness - Belgrade** (5€/day)
- Objective: OUTCOME_AWARENESS, optimization: THRUPLAY
- Ad Set: Belgrade, Women 18-45, FB + IG placements
- 3 Rori video ads (VS, Caudalie, ABH) + 4 Partnership Ads
- Partnership ads: @la_reina_dulce, @lady_withhat, @mamma.m.i.a, @viviennesabo.serbia

**Campaign 2: Rori Catalog Retarget - Belgrade** (5€/day)
- Objective: OUTCOME_SALES, optimization: OFFSITE_CONVERSIONS (Purchase)
- Retargets: video viewers 50% + IG engagers + page engagers
- DPA with 175 products (VS + Caudalie + ABH)

### Legacy Campaigns Paused
- PFM_WEB_Traffic (was spending 10€/day on all of Serbia — paused)
- All other legacy campaigns already paused

### Pixel-Catalog Fix
- Pixel `555063416919437` was NOT connected to catalog `2543619572695742`.
- Connected it — critical for DPA to match pixel events with catalog products.
- Verified: `content_ids` in pixel events (product.id) match `retailer_id` in catalog.

### Pixel Events Status
- `PageView`: ✅ active (~560/day)
- `ViewContent`: ✅ active (~60/day)
- `AddToCart`: ⚠️ code exists, fires on login+consent, low volume expected
- `InitiateCheckout`: ⚠️ code exists, same conditions
- `Purchase`: ⚠️ code exists, same conditions

### Influencer Partners
| Username | Status | Brands |
|----------|--------|--------|
| @la_reina_dulce | Active | VS, Rori |
| @katarina.munjic | Active | Rori |
| @bojana.tomic | Active | VS |
| @lady_withhat | Active | Rori |
| @viviennesabo.serbia | Active | VS |
| @milica_kontic92 | Pending | Caudalie |
| @mamma.m.i.a | Active | Caudalie |
| @jovanaradovanovicmakeup | Active | VS |

46 reels eligible for partnership ads, 4 blocked (copyrighted music).

### Monitoring
- Daily Slack report set up via GitHub Actions (08:00 CET).
- Reports: campaign performance, ad-level breakdown, pixel events.
- Webhook stored as `SLACK_WEBHOOK_URL` secret.

---

## Expected Metrics (first 30 days)

| Metric | Awareness | Catalog Retarget |
|--------|-----------|-----------------|
| CPM | 2-5€ | 3-8€ |
| ThruPlay cost | 0.01-0.03€ | — |
| CTR | 1-3% | 1-3% |
| CPC | — | 0.05-0.20€ |
| ROAS target | — | 3x+ |

### Decision Points
- **Day 7**: Compare partnership ads vs Rori video ads — kill losers.
- **Day 14**: If retarget audience > 1000, create Lookalike.
- **Day 14**: If ROAS > 2x, consider increasing budget.
- **Day 30**: Full review and strategy adjustment.

---

## 2026-03-23 — 30-Day Review & Campaign Optimization

### Performance Analysis (21 Feb — 22 Mar)

**Brand Awareness - Belgrade** (5€/day budget, €18.15 spent):
| Ad | Impressions | Reach | Spend | Video Views | ThruPlays | CTR | CPM |
|----|-------------|-------|-------|-------------|-----------|-----|-----|
| @viviennesabo.serbia Cabaret | 22,234 | 18,547 | €12.87 | 7,823 | 3,499 | 0.22% | €0.58 |
| VS - Olovka i ulje za usne | 4,035 | 3,836 | €2.89 | 2,291 | 632 | 0.62% | €0.72 |
| @mamma.m.i.a Caudalie | 521 | 521 | €0.59 | 160 | 52 | 0.19% | €1.13 |
| @lady_withhat Rori | 458 | 438 | €0.28 | 170 | 41 | 0.44% | €0.61 |
| Caudalie - Kozmetika | 401 | 361 | €0.90 | 257 | 226 | 1.25% | €2.24 |
| @la_reina_dulce VS | 383 | 371 | €0.43 | 206 | 94 | 0.78% | €1.12 |
| ABH - Anastasia BH | 88 | 84 | €0.19 | 62 | 56 | 0% | €2.16 |

**Catalog Retarget - Belgrade** (5€/day budget, €0.38 spent):
- 56 impressions, 4 reach, 0 clicks — effectively dead.

### Key Findings
- VS Cabaret partnership consumed 71% of total budget and 79% of impressions — starving other ads.
- Total spend €18.53 of possible ~€300 (6% utilization) — Meta under-delivering significantly.
- Catalog Retarget failed because: optimization goal `OFFSITE_CONVERSIONS (PURCHASE)` requires conversion signals, but pixel has near-zero purchase events. Audience too small (~1,000 per audience). `Page Engagers 30d` audience flagged as too small for delivery (code 300).
- Pixel volume much lower than expected: PageView ~10-20/day (not ~560/day as initially measured), ViewContent ~1-3/day.

### Actions Taken

**1. Paused @viviennesabo.serbia Cabaret ad** (ID: 120242238054790751)
- Reason: consuming 79% of all impressions, starving other 6 ads.
- Expected: remaining ads will get more even distribution.

**2. Replaced Catalog Retarget adset**
- **Paused**: old adset `Retarget Engagers - All Influencer Brands` (ID: 120242237747130751)
  - Problem: `OFFSITE_CONVERSIONS (PURCHASE)` optimization with zero purchase signals = no delivery.
- **Created**: new adset `Retarget Engagers - Link Clicks Optimized` (ID: 120242378319210751)
  - Optimization: `LINK_CLICKS` — Meta finds people who will click, not wait for purchase signal.
  - **Advantage Audience enabled** — Meta expands beyond custom audiences to similar users.
  - Age range: 18-65 (required by Advantage Audience, Meta still favors 18-45 from seed audiences).
  - Same audiences: IG Engagers 30d + All Brands Video Viewers 50%.
  - Removed: Page Engagers 30d (too small, delivery_status 300).
  - Same budget: 5€/day.
- **Created**: new DPA ad `DPA Influencer Brands - Link Clicks` (ID: 120242378372620751)
  - Same creative: 175 products (VS + Caudalie + ABH), SHOP_NOW CTA.

**3. Meta API integrated into Rori admin panel**
- Backend: `GET /meta/campaigns` endpoint on rori-core (branch: `newcore-marketing`).
- Frontend: "Ads" tab added to `/materials` page (branch: `newfront-marketing`).
- `META_ACCESS_TOKEN` and `META_AD_ACCOUNT_ID` added to GitHub Environment Secrets (dev) and deploy workflow.
- Purpose: expose Meta token in server env for AI agent access + campaign visibility in admin panel.

### Current Active State

**Brand Awareness** (6 active ads, was 7):
- @lady_withhat Rori, @mamma.m.i.a Caudalie, @la_reina_dulce VS (partnerships)
- VS Olovka i ulje, Caudalie Kozmetika, ABH Anastasia BH (brand videos)
- PAUSED: @viviennesabo.serbia Cabaret

**Catalog Retarget** (1 active ad, new adset):
- DPA Influencer Brands - Link Clicks (Advantage Audience enabled)

### Next Steps
- **Day 1-3**: Monitor new catalog retarget adset — expect significantly higher delivery.
- **Day 7**: Check if awareness ads redistribute evenly without VS Cabaret.
- Investigate low pixel volume — may need to verify pixel firing on rori.app production.
- Consider creating website visitors custom audience when ToS is accepted in Meta Business Manager.
