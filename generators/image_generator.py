from pathlib import Path
from datetime import datetime, date
from config.dnh_brand import BRANCHES, ROOM_TYPES, BRAND

# ─── Tema Berdasarkan Hari ───────────────────────────────────────────────────

DAY_THEMES = {
0: {  # Senin
“theme”: “productive monday staycation”,
“vibe”: “fresh start, work from apartment, morning coffee vibes”,
“copy”: “Mulai minggu dengan tenang. Staycation buat yang butuh fokus.”,
},
1: {  # Selasa
“theme”: “midweek escape”,
“vibe”: “quiet apartment, city view, calm and cozy”,
“copy”: “Di tengah pekan yang padat, istirahat sebentar itu perlu.”,
},
2: {  # Rabu
“theme”: “hump day relaxation”,
“vibe”: “relaxing evening, apartment lounge, warm lighting”,
“copy”: “Rabu sore paling enak dihabiskan di kamar yang nyaman.”,
},
3: {  # Kamis
“theme”: “pre-weekend staycation”,
“vibe”: “excitement, almost weekend, couple or solo traveler”,
“copy”: “Besok weekend — kenapa nggak mulai dari sekarang?”,
},
4: {  # Jumat
“theme”: “TGIF weekend getaway”,
“vibe”: “celebration, end of week, fun nightlife Bandung”,
“copy”: “Akhir pekan tiba! Rayakan di apartemen terbaik Bandung.”,
},
5: {  # Sabtu
“theme”: “romantic saturday night date staycation”,
“vibe”: “couple quality time, malam mingguan, cozy room, candle dinner vibes, Bandung night view”,
“copy”: “Malam Minggu paling berkesan? Staycation berdua di DNH.”,
},
6: {  # Minggu
“theme”: “lazy sunday family staycation”,
“vibe”: “family time, relaxing morning, breakfast in bed, kids-friendly”,
“copy”: “Minggu santai bareng keluarga — semua tersedia di sini.”,
},
}

# ─── Momen Spesial ────────────────────────────────────────────────────────────

SPECIAL_MOMENTS = [
# (bulan, tanggal, nama, tema visual, copy)
(1,  1,  “Tahun Baru”,         “new year celebration fireworks, city skyline Bandung, champagne toast, luxury apartment”, “Rayakan tahun baru di ketinggian kota Bandung.”),
(2,  14, “Valentine”,          “romantic valentine couple, rose petals, candlelight dinner, cozy studio apartment”, “Rayakan cinta di tempat yang istimewa.”),
(4,  10, “Eid Al-Fitr”,        “Eid Mubarak festive, family warmth, ketupat decoration, Indonesian culture, apartment celebration”, “Selamat Hari Raya — rayakan bersama orang tersayang.”),
(5,  1,  “Hari Buruh”,         “workers rest day, staycation solo, relax recharge, peaceful morning apartment”, “Hari buruh = hari istirahat. Kamu layak recharge.”),
(6,  1,  “Hari Anak”,          “children day, family fun, kids playing, cheerful colorful apartment”, “Hari anak yang paling berkesan dimulai dari sini.”),
(8,  17, “HUT RI”,             “Indonesia independence day, red white decoration, patriotic celebration apartment Bandung”, “Rayakan kemerdekaan dengan penginapan terbaik lokal.”),
(10, 31, “Halloween”,          “halloween night spooky fun, orange purple aesthetic, cozy apartment party”, “Malam yang berbeda di tempat yang luar biasa.”),
(12, 24, “Malam Natal”,        “christmas eve cozy apartment, warm string lights, festive decoration, family gathering”, “Malam Natal paling hangat — di tempat yang terasa seperti rumah.”),
(12, 31, “Malam Tahun Baru”,   “new year eve countdown, fireworks city view Bandung, celebration couple rooftop vibes”, “Sambut tahun baru dari sudut terbaik Bandung.”),
]

def get_moment_override(today: date = None):
“”“Cek apakah hari ini ada momen spesial. Return override dict atau None.”””
if today is None:
today = date.today()
for (bulan, tanggal, nama, tema, copy) in SPECIAL_MOMENTS:
if today.month == bulan and today.day == tanggal:
return {“nama”: nama, “theme”: tema, “copy”: copy}
return None

class ImageGenerator:
def **init**(self, **kwargs):
pass

```
def generate(self, branch, room_type, theme=None, style="luxury"):
    today = date.today()
    moment = get_moment_override(today)
    day_info = DAY_THEMES[today.weekday()]
    day_name = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][today.weekday()]

    if moment:
        context_theme = moment["theme"]
        context_copy = moment["copy"]
        context_label = f"✨ Momen Spesial: {moment['nama']}"
    else:
        context_theme = day_info["theme"]
        context_copy = day_info["copy"]
        context_label = f"📅 Hari {day_name}"

    prompt = self._build_prompt(branch, room_type, context_theme, style)

    return {
        "success": True,
        "source": "prompt_only",
        "prompt": prompt,
        "context_label": context_label,
        "copy_suggestion": context_copy,
        "platforms": {
            "dalle": "https://chat.openai.com",
            "leonardo": "https://app.leonardo.ai",
            "nanobanana": "https://nanobanana.com",
        }
    }

def format_telegram_message(self, result):
    if not result.get("success"):
        return "⚠️ Gagal membuat prompt gambar."

    prompt = result["prompt"]
    platforms = result["platforms"]
    label = result.get("context_label", "")
    copy_hint = result.get("copy_suggestion", "")

    return (
        f"🎨 *Prompt Poster Hari Ini*\n"
        f"{label}\n\n"
        f"`{prompt}`\n\n"
        f"💬 *Saran copy caption:*\n_{copy_hint}_\n\n"
        f"📋 *Generate di:*\n"
        f"• [DALL-E]({platforms['dalle']})\n"
        f"• [Leonardo AI]({platforms['leonardo']})\n"
        f"• [NanoBanana]({platforms['nanobanana']})"
    )

def _build_prompt(self, branch, room_type, context_theme, style):
    b = BRANCHES.get(branch, BRANCHES["gateway"])
    r = ROOM_TYPES.get(room_type, ROOM_TYPES["studio"])
    return (
        f"Instagram poster, {context_theme}, "
        f"{b['name']} Bandung apartment, "
        f"{r['name']} room {r['size']}, "
        f"{style} style, premium hospitality Indonesia, "
        f"clean modern layout, warm golden lighting, "
        f"professional photography, "
        f"brand accent color {BRAND['primary_color']}, "
        f"no watermark, no text overlay, "
        f"portrait 4:5 ratio 1080x1350px."
    )
```
