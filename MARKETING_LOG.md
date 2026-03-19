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
