from datetime import datetime

WEEKLY_THEMES = {
    0: {"day_name": "Senin",  "theme": "workspace",   "theme_name": "Workspace Monday 💼",   "branch": "gateway",    "room_type": "studio", "tone": "professional", "style": "modern"},
    1: {"day_name": "Selasa", "theme": "room_tour",   "theme_name": "Room Tour Tuesday 🏠",   "branch": "jarrdin",    "room_type": "1br",    "tone": "relatable",    "style": "cozy"},
    2: {"day_name": "Rabu",   "theme": "wellness",    "theme_name": "Wellness Wednesday 🧘",  "branch": "grand_asia", "room_type": "2br",    "tone": "aspirational", "style": "luxury"},
    3: {"day_name": "Kamis",  "theme": "testimonial", "theme_name": "Testimonial Thursday 💬","branch": "gateway",    "room_type": "studio", "tone": "relatable",    "style": "cozy"},
    4: {"day_name": "Jumat",  "theme": "weekend",     "theme_name": "Friday Vibes 🎉",        "branch": "jarrdin",    "room_type": "studio", "tone": "humor",        "style": "modern"},
    5: {"day_name": "Sabtu",  "theme": "promo",       "theme_name": "Weekend Promo 🌟",       "branch": "grand_asia", "room_type": "2br",    "tone": "exciting",     "style": "luxury"},
    6: {"day_name": "Minggu", "theme": "family",      "theme_name": "Family Sunday 👨‍👩‍👧",      "branch": "gateway",    "room_type": "2br",    "tone": "warm",         "style": "cozy"},
}

def get_today_theme():
    return WEEKLY_THEMES[datetime.now().weekday()]

def get_custom_theme(theme_key):
    for entry in WEEKLY_THEMES.values():
        if entry["theme"] == theme_key:
            return entry
    return WEEKLY_THEMES[5]
