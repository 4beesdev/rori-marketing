"""Central configuration for all Meta Marketing API resources.

All IDs, audiences, product sets, and campaign structures in one place.
Updated by AI agents and campaign management scripts.
"""

# === Meta Account IDs ===
AD_ACCOUNT_ID = "act_451952937265646"
BUSINESS_ID = "1693182164399002"
PAGE_ID = "383041474901753"
IG_ACCOUNT_ID = "17841452496126909"
PIXEL_ID = "555063416919437"
CATALOG_ID = "2543619572695742"

# === Product Sets ===
PRODUCT_SETS = {
    "all": {"id": "1630772897472470", "name": "All Products", "count": 2801},
    "vivienne_sabo": {"id": "957383383629326", "name": "Vivienne Sabo", "count": 144},
    "caudalie": {"id": "26711159618470309", "name": "Caudalie", "count": 16},
    "abh": {"id": "790185514136659", "name": "Anastasia Beverly Hills", "count": 15},
    "influencer_brands": {
        "id": "3854033414900814",
        "name": "VS + Caudalie + ABH (Influencer Brands)",
        "count": 175,
    },
}

# === Custom Audiences ===
AUDIENCES = {
    "ig_engagers_30d": {
        "id": "120242237614610751",
        "name": "Rori IG Engagers 30d",
        "type": "engagement",
        "source": "ig_business",
    },
    "page_engagers_30d": {
        "id": "120242237616080751",
        "name": "Rori Page Engagers 30d",
        "type": "engagement",
        "source": "page",
    },
    "vs_video_viewers_50pct": {
        "id": "120242237649310751",
        "name": "VS Video Viewers 50pct",
        "type": "video",
        "video_ids": ["939922962041417", "936458855372977", "865421319704880"],
    },
    "caudalie_video_viewers_50pct": {
        "id": "120242237651680751",
        "name": "Caudalie Video Viewers 50pct",
        "type": "video",
        "video_ids": ["1979530679328463", "755407817632820", "856099000747849", "601886096297320"],
    },
    "abh_video_viewers_50pct": {
        "id": "120242237654210751",
        "name": "ABH Video Viewers 50pct",
        "type": "video",
        "video_ids": ["1231460788304862"],
    },
    "all_brands_video_viewers_50pct": {
        "id": "120242237655790751",
        "name": "All Influencer Brands Video Viewers 50pct",
        "type": "video",
    },
}

# === Active Campaigns ===
CAMPAIGNS = {
    "awareness": {
        "id": "120242237693510751",
        "name": "Rori Brand Awareness - Belgrade",
        "objective": "OUTCOME_AWARENESS",
        "daily_budget_cents": 500,
        "adset_id": "120242237719180751",
        "targeting": {
            "city": "Belgrade",
            "city_key": "2673746",
            "gender": "female",
            "age_min": 18,
            "age_max": 45,
        },
        "ads": {
            "vs_video": "120242237782670751",
            "caudalie_video": "120242237791110751",
            "abh_video": "120242237793050751",
            "partnership_la_reina_dulce": "120242238045460751",
            "partnership_lady_withhat": "120242238046370751",
            "partnership_mamma_mia": "120242238050250751",
            "partnership_viviennesabo_cabaret": "120242238054790751",
        },
    },
    "catalog_retarget": {
        "id": "120242237739870751",
        "name": "Rori Catalog Retarget - Belgrade",
        "objective": "OUTCOME_SALES",
        "daily_budget_cents": 500,
        "adset_id": "120242237747130751",
        "product_set": "influencer_brands",
        "retarget_audiences": [
            "all_brands_video_viewers_50pct",
            "ig_engagers_30d",
            "page_engagers_30d",
        ],
        "ads": {
            "dpa_influencer_brands": "120242237797140751",
        },
    },
}

# === Paused (Legacy) Campaigns ===
PAUSED_CAMPAIGNS = {
    "vs_aware": "120239417360170751",
    "pfm_rori_engagement": "120218306078750751",
    "pfm_rori_awareness": "120214365118610751",
    "pfm_web_traffic": "120213736032630751",
    "pfm_rus_traffic": "120213424548180751",
    "pfm_appevents_catalog": "120213366309390751",
    "pfm_ios14_apppromote": "120213137159500751",
    "pfm_mof_apppromote": "120213059481510751",
    "pfm_tof_apppromote": "120213006562520751",
}

# === Influencer Partners ===
INFLUENCER_PARTNERS = {
    "la_reina_dulce": {"ig_id": "17841401849386552", "status": "active", "brands": ["VS", "Rori"]},
    "katarina_munjic": {"ig_id": "17841401361857038", "status": "active", "brands": ["Rori"]},
    "bojana_tomic": {"ig_id": "17841401348071880", "status": "active", "brands": ["VS"]},
    "lady_withhat": {"ig_id": "17841401649992701", "status": "active", "brands": ["Rori"]},
    "viviennesabo_serbia": {"ig_id": "17841476798155747", "status": "active", "brands": ["VS"]},
    "milica_kontic92": {"ig_id": "17841402094180677", "status": "pending", "brands": ["Caudalie"]},
    "mamma_mia": {"ig_id": "17841401878813194", "status": "active", "brands": ["Caudalie"]},
    "jovanaradovanovicmakeup": {"ig_id": "17841403156811935", "status": "active", "brands": ["VS"]},
}

# === Brand Landing Pages ===
BRAND_URLS = {
    "vivienne_sabo": "https://rori.app/rs/brands/vivienne-sab%C3%B3-527",
    "caudalie": "https://rori.app/rs/brands/caudalie-480",
    "abh": "https://rori.app/rs/brands/anastasia-beverly-hills-511",
}

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
