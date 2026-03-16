import os
import requests
import tempfile
import urllib.parse
from config.dnh_brand import BRANCHES, ROOM_TYPES, BRAND


class ImageGenerator:
    def __init__(self):
        self.pollinations_url = "https://image.pollinations.ai/prompt"

    def generate(self, branch, room_type, theme, style):
        """Generate poster: image via Pollinations AI + fallback prompt text"""
        branch_info = BRANCHES.get(branch, BRANCHES["gateway"])
        room_info   = ROOM_TYPES.get(room_type, ROOM_TYPES["studio"])
        brand_name  = BRAND.get("name", "DNH Property")

        style_prompts = {
            "luxury":    "luxurious elegance, gold accents, marble textures, premium furniture, ambient warm lighting, sophisticated atmosphere",
            "cozy":      "warm cozy atmosphere, soft textiles, ambient fairy lights, homely feeling, comfortable furniture, inviting space",
            "modern":    "contemporary modern design, clean lines, minimalist aesthetic, smart home features, sleek furniture, neutral tones",
            "minimalist":"minimalist design, clean white spaces, simple furniture, natural light, decluttered aesthetic, zen atmosphere",
        }

        theme_enhancements = {
            "workspace":   "home office setup, ergonomic desk, laptop, productive ambiance, natural lighting for work",
            "weekend":     "relaxing weekend vibes, leisure setup, entertainment area, cozy corner for unwinding",
            "promo":       "special offer display, attractive promotional elements, festive decoration, celebratory atmosphere",
            "room_tour":   "full room showcase, detailed interior view, every corner visible, architectural highlights",
            "testimonial": "satisfied guest experience, welcoming entrance, memorable stay moments, guest-friendly amenities",
            "family":      "family-friendly space, extra bedding setup, kids-friendly area, spacious living for families",
            "wellness":    "wellness retreat vibes, spa-like bathroom, meditation corner, self-care amenities, relaxing ambiance",
        }

        style_desc = style_prompts.get(style, style_prompts["luxury"])
        theme_desc = theme_enhancements.get(theme, "")

        prompt = (
            f"Professional real estate photography, {style} style, "
            f"{room_info['name']} apartment at {branch_info['name']} Bandung Indonesia. "
            f"Room size {room_info['size']}, capacity {room_info['capacity']}. "
            f"{style_desc}. {theme_desc}. "
            f"Location vibe: {branch_info['vibe']}. "
            f"High quality 4K photorealistic, interior design magazine worthy, "
            f"wide angle lens, balanced natural and artificial lighting, gold accent color, "
            f"brand {brand_name}, no text overlay, no watermark"
        )

        context_label = f"🎨 {branch_info['name']} · {room_info['name']} ({style.title()})"

        # Generate actual image
        image_path = self._generate_image(prompt)

        return {
            "success":       True,
            "prompt":        prompt,
            "context_label": context_label,
            "image_path":    image_path,   # None jika gagal
            "branch":        branch,
            "room_type":     room_type,
            "theme":         theme,
            "style":         style,
            "metadata": {
                "branch_name": branch_info["name"],
                "room_name":   room_info["name"],
                "room_size":   room_info["size"],
                "capacity":    room_info["capacity"],
                "location":    branch_info["location"],
            },
        }

    def _generate_image(self, prompt: str) -> str | None:
        """
        Generate gambar via Pollinations AI (gratis, tanpa API key).
        Return path file temporer, atau None jika gagal.
        Format 9:16 (1080×1920) cocok untuk IG Stories / poster vertikal.
        """
        try:
            encoded = urllib.parse.quote(prompt)
            url = (
                f"{self.pollinations_url}/{encoded}"
                f"?width=1080&height=1920&model=flux&nologo=true&seed=-1"
            )
            print(f"[ImageGenerator] Generating via Pollinations AI...")
            resp = requests.get(url, timeout=90)   # Pollinations kadang lambat
            resp.raise_for_status()

            content_type = resp.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                print(f"[ImageGenerator] Response bukan gambar: {content_type}")
                return None

            suffix = ".jpg" if "jpeg" in content_type else ".png"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(resp.content)
            tmp.close()
            print(f"[ImageGenerator] Gambar tersimpan: {tmp.name} ({len(resp.content)//1024} KB)")
            return tmp.name

        except Exception as e:
            print(f"[ImageGenerator] Pollinations error: {e}")
            return None
