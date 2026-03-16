import os
from config.dnh_brand import BRANCHES, ROOM_TYPES, BRAND

class ImageGenerator:
    def __init__(self):
        pass

    def generate(self, branch, room_type, theme, style):
        """Generate poster prompt for DNH Property"""
        branch_info = BRANCHES.get(branch, BRANCHES["gateway"])
        room_info = ROOM_TYPES.get(room_type, ROOM_TYPES["studio"])
        brand_name = BRAND.get("name", "DNH Property")
        primary_color = BRAND.get("primary_color", "#c9a84c")

        # Style templates
        style_prompts = {
            "luxury": "luxurious elegance, gold accents, marble textures, premium furniture, ambient warm lighting, sophisticated atmosphere",
            "cozy": "warm cozy atmosphere, soft textiles, ambient fairy lights, homely feeling, comfortable furniture, inviting space",
            "modern": "contemporary modern design, clean lines, minimalist aesthetic, smart home features, sleek furniture, neutral tones",
            "minimalist": "minimalist design, clean white spaces, simple furniture, natural light, decluttered aesthetic, zen atmosphere"
        }

        # Theme enhancements
        theme_enhancements = {
            "workspace": "home office setup, ergonomic desk, laptop, productive ambiance, natural lighting for work",
            "weekend": "relaxing weekend vibes, leisure setup, entertainment area, cozy corner for unwinding",
            "promo": "special offer display, attractive promotional elements, festive decoration, celebratory atmosphere",
            "room_tour": "full room showcase, detailed interior view, every corner visible, architectural highlights",
            "testimonial": "satisfied guest experience, welcoming entrance, memorable stay moments, guest-friendly amenities",
            "family": "family-friendly space, extra bedding setup, kids-friendly area, spacious living for families",
            "wellness": "wellness retreat vibes, spa-like bathroom, meditation corner, self-care amenities, relaxing ambiance"
        }

        style_desc = style_prompts.get(style, style_prompts["luxury"])
        theme_desc = theme_enhancements.get(theme, "")

        prompt = (
            f"Professional real estate photography, {style} style, "
            f"{room_info['name']} apartment at {branch_info['name']} Bandung. "
            f"Room size: {room_info['size']}, capacity: {room_info['capacity']}. "
            f"{style_desc}. {theme_desc}. "
            f"Location vibe: {branch_info['vibe']}. "
            f"High quality, 4K resolution, photorealistic, interior design magazine worthy, "
            f"shot with wide angle lens, natural and artificial lighting balance, "
            f"accent color hints of {primary_color}, brand: {brand_name}"
        )

        context_label = f"🎨 {branch_info['name']} - {room_info['name']} ({style.title()})"

        copy_suggestion = (
            "Salin prompt di atas dan generate gambar di:\n"
            "• Leonardo AI → app.leonardo.ai\n"
            "• DALL-E 3 → chat.openai.com\n"
            "• Midjourney → midjourney.com"
        )

        return {
            "success": True,
            "prompt": prompt,
            "context_label": context_label,
            "copy_suggestion": copy_suggestion,
            "branch": branch,
            "room_type": room_type,
            "theme": theme,
            "style": style,
            "metadata": {
                "branch_name": branch_info["name"],
                "room_name": room_info["name"],
                "room_size": room_info["size"],
                "capacity": room_info["capacity"],
                "location": branch_info["location"]
            }
        }
