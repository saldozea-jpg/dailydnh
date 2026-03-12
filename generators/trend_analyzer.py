from config.dnh_brand import BRAND

STATIC_TRENDS = {
    "workspace":   {"hashtags": [{"tag": "WorkFromApartment", "views": "45.2K"}, {"tag": "WFHBandung", "views": "28.1K"}, {"tag": "DigitalNomadBandung", "views": "19.5K"}], "audio": [{"name": "Lo-fi Morning Focus"}]},
    "weekend":     {"hashtags": [{"tag": "StaycationBandung", "views": "120.5K"}, {"tag": "WeekendGetaway", "views": "89.3K"}, {"tag": "BandungWeekend", "views": "54.2K"}], "audio": [{"name": "Friday Night Vibes"}]},
    "promo":       {"hashtags": [{"tag": "PromoHotelBandung", "views": "67.8K"}, {"tag": "ApartemenMurahBandung", "views": "43.2K"}, {"tag": "StaycationMurah", "views": "98.1K"}], "audio": [{"name": "Upbeat Promo Vibes"}]},
    "room_tour":   {"hashtags": [{"tag": "RoomTour", "views": "250.3K"}, {"tag": "ApartemenBandung", "views": "180.2K"}, {"tag": "InteriorApartemen", "views": "76.4K"}], "audio": [{"name": "Aesthetic Room Tour BGM"}]},
    "testimonial": {"hashtags": [{"tag": "ReviewHotelBandung", "views": "55.1K"}, {"tag": "StaycationReview", "views": "42.7K"}, {"tag": "RekomendasiBandung", "views": "88.9K"}], "audio": [{"name": "Chill Testimonial Vibes"}]},
    "family":      {"hashtags": [{"tag": "FamilyStaycation", "views": "62.3K"}, {"tag": "LiburanKeluarga", "views": "48.5K"}, {"tag": "BandungFamilyTrip", "views": "35.2K"}], "audio": [{"name": "Happy Family BGM"}]},
    "wellness":    {"hashtags": [{"tag": "WellnessStaycation", "views": "38.9K"}, {"tag": "SelfCareBandung", "views": "29.4K"}, {"tag": "RelaxApartemen", "views": "21.7K"}], "audio": [{"name": "Zen Morning Sounds"}]},
}

class TrendAnalyzer:
    def get_trending(self, theme=None):
        base = STATIC_TRENDS.get(theme, STATIC_TRENDS["weekend"])
        branded = [{"tag": t.replace("#", ""), "views": "---"} for t in BRAND["hashtags"]["branded"]]
        return {"hashtags": base["hashtags"] + branded, "audio": base["audio"]}

    def analyze(self, theme=None):
        return self.get_trending(theme)
