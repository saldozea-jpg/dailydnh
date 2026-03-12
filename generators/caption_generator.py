import os
import requests
from config.dnh_brand import BRANCHES, ROOM_TYPES, PROMOS, BRAND

class CaptionGenerator:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    def generate(self, theme, branch, room_type, tone, trends):
        if not self.api_key:
            raise ValueError("GROQ_API_KEY tidak ditemukan.")
        b = BRANCHES.get(branch, BRANCHES["gateway"])
        r = ROOM_TYPES.get(room_type, ROOM_TYPES["studio"])
        promo = PROMOS.get("malam", {})
        hashtag_list = [f"#{h['tag']}" for h in trends.get("hashtags", [])]
        branded_tags = BRAND["hashtags"]["branded"] + BRAND["hashtags"]["location"] + BRAND["hashtags"]["general"]
        all_tags = " ".join(hashtag_list + branded_tags)

        prompt = (
            f"Kamu adalah copywriter properti premium Indonesia.\n"
            f"Buat caption Instagram untuk DNH Property Bandung.\n"
            f"Cabang: {b['name']} | Kamar: {r['name']} ({r['size']}) | Tema: {theme} | Tone: {tone}\n"
            f"Promo malam: check-in {promo.get('checkin','20:00')}, checkout {promo.get('checkout','12:00')}, Studio Rp200rb\n\n"
            f"Format:\n1. HOOK\n2. BODY (2-3 kalimat)\n3. CTA\n4. HASHTAG: {all_tags}\n\n"
            f"Bahasa Indonesia, hangat dan premium, max 2200 karakter."
        )
        try:
            resp = requests.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 600, "temperature": 0.85},
                timeout=30
            )
            resp.raise_for_status()
            full_text = resp.json()["choices"][0]["message"]["content"]
            return {"full_text": full_text, "hashtags": hashtag_list + branded_tags, "fallback": False}
        except Exception as e:
            print(f"[CaptionGenerator] Error: {e}")
            return {"full_text": f"🏨 {b['name']} Bandung\nKamar {r['name']} tersedia!\nDM untuk booking. {' '.join(branded_tags[:5])}", "hashtags": branded_tags, "fallback": True}
