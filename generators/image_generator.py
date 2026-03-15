from datetime import date
from config.dnh_brand import BRANCHES, ROOM_TYPES, BRAND

DAY_THEMES = {
0: {
“theme”: “productive monday staycation”,
“copy”: “Mulai minggu dengan tenang. Staycation buat yang butuh fokus.”,
},
1: {
“theme”: “midweek escape”,
“copy”: “Di tengah pekan yang padat, istirahat sebentar itu perlu.”,
},
2: {
“theme”: “hump day relaxation”,
“copy”: “Rabu sore paling enak dihabiskan di kamar yang nyaman.”,
},
3: {
“theme”: “pre-weekend staycation”,
“copy”: “Besok weekend, kenapa nggak mulai dari sekarang?”,
},
4: {
“theme”: “TGIF weekend getaway”,
“copy”: “Akhir pekan tiba! Rayakan di apartemen terbaik Bandung.”,
},
5: {
“theme”: “romantic saturday night date staycation, couple quality time, malam mingguan, candle dinner vibes, Bandung night view”,
“copy”: “Malam Minggu paling berkesan? Staycation berdua di DNH.”,
},
6: {
“theme”: “lazy sunday family staycation, family time, relaxing morning, breakfast in bed”,
“copy”: “Minggu santai bareng keluarga, semua tersedia di sini.”,
},
}

SPECIAL_MOMENTS = [
(1,  1,  “Tahun Baru”,       “new year celebration fireworks, city skyline Bandung, champagne toast, luxury apartment”, “Rayakan tahun baru di ketinggian kota Bandung.”),
(2,  14, “Valentine”,        “romantic valentine couple, rose petals, candlelight dinner, cozy studio apartment”, “Rayakan cinta di tempat yang istimewa.”),
(4,  10, “Eid Al-Fitr”,      “Eid Mubarak festive, family warmth, ketupat decoration, Indonesian culture”, “Selamat Hari Raya, rayakan bersama orang tersayang.”),
(5,  1,  “Hari Buruh”,       “workers rest day, staycation solo, relax recharge, peaceful morning apartment”, “Hari buruh sama dengan hari istirahat. Kamu layak recharge.”),
(6,  1,  “Hari Anak”,        “children day, family fun, kids playing, cheerful colorful apartment”, “Hari anak yang paling berkesan dimulai dari sini.”),
(8,  17, “HUT RI”,           “Indonesia independence day, red white decoration, patriotic celebration apartment Bandung”, “Rayakan kemerdekaan dengan penginapan terbaik lokal.”),
(10, 31, “Halloween”,        “halloween night spooky fun, orange purple aesthetic, cozy apartment party”, “Malam yang berbeda di tempat yang luar biasa.”),
(12, 24, “Malam Natal”,      “christmas eve cozy apartment, warm string lights, festive decoration, family gathering”, “Malam Natal paling hangat di tempat yang terasa seperti rumah.”),
(12, 31, “Malam Tahun Baru”, “new year eve countdown, fireworks city view Bandung, celebration couple rooftop vibes”, “Sambut tahun baru dari sudut terbaik Bandung.”),
]

def get_moment_override(today=None):
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
    day_names = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    day_name = day_names[today.weekday()]

    if moment:
        context_theme = moment["theme"]
        context_copy = moment["copy"]
        context_label = "Momen Spesial: " + moment["nama"]
    else:
        context_theme = day_info["theme"]
        context_copy = day_info["copy"]
        context_label = "Hari " + day_name

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
        return "Gagal membuat prompt gambar."
    prompt = result["prompt"]
    platforms = result["platforms"]
    label = result.get("context_label", "")
    copy_hint = result.get("copy_suggestion", "")
    return (
        "Prompt Poster Hari Ini\n"
        + label + "\n\n"
        + prompt + "\n\n"
        + "Saran caption: " + copy_hint + "\n\n"
        + "Generate di:\n"
        + "DALL-E: " + platforms["dalle"] + "\n"
        + "Leonardo: " + platforms["leonardo"] + "\n"
        + "NanoBanana: " + platforms["nanobanana"]
    )

def _build_prompt(self, branch, room_type, context_theme, style):
    b = BRANCHES.get(branch, BRANCHES["gateway"])
    r = ROOM_TYPES.get(room_type, ROOM_TYPES["studio"])
    return (
        "Instagram poster, " + context_theme + ", "
        + b["name"] + " Bandung apartment, "
        + r["name"] + " room " + r["size"] + ", "
        + style + " style, premium hospitality Indonesia, "
        + "clean modern layout, warm golden lighting, "
        + "professional photography, "
        + "brand accent color " + BRAND["primary_color"] + ", "
        + "no watermark, no text overlay, "
        + "portrait 4:5 ratio 1080x1350px."
    )
```
