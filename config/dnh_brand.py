BRANCHES = {
    "gateway": {
        "name": "Gateway Pasteur",
        "location": "Jl. Dr. Djundjunan, Pasteur, Bandung",
        "vibe": "modern business traveler",
        "best_for": "Business travelers, transit passengers"
    },
    "jarrdin": {
        "name": "Jarrdin Cihampelas",
        "location": "Cihampelas, Bandung",
        "vibe": "young lifestyle",
        "best_for": "Young couples, friends, food enthusiasts"
    },
    "grand_asia": {
        "name": "Grand Asia Afrika",
        "location": "Asia Afrika, Bandung",
        "vibe": "luxury heritage",
        "best_for": "Families, heritage tourists, luxury seekers"
    },
}

ROOM_TYPES = {
    "studio": {"name": "Studio",    "size": "24 m²", "capacity": "1-2 orang", "price_range": "280K-350K"},
    "1br":    {"name": "1 Bedroom", "size": "33 m²", "capacity": "2-3 orang", "price_range": "380K-450K"},
    "2br":    {"name": "2 Bedroom", "size": "50 m²", "capacity": "4-5 orang", "price_range": "550K-700K"},
}

PROMOS = {
    "malam": {
        "label": "Promo Malam",
        "checkin": "20:00",
        "checkout": "12:00",
        "price": {"studio": 200000},
        "valid_days": ["Minggu", "Senin", "Selasa", "Rabu", "Kamis"],
        "note": "Tidak berlaku Jumat & Sabtu malam"
    }
}

BRAND = {
    "name": "DNH Property",
    "tagline": "Live Beyond Ordinary",
    "primary_color": "#c9a84c",
    "hashtags": {
        "branded":  ["#DNHProperty", "#LiveBeyondOrdinary"],
        "location": ["#GatewayPasteur", "#JarrdinCihampelas", "#GrandAsiaAfrika"],
        "general":  ["#StaycationBandung", "#ApartemenBandung", "#BandungTrip"]
    }
}
