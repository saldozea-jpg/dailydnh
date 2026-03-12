import requests
from urllib.parse import quote
from pathlib import Path
from datetime import datetime
from config.dnh_brand import BRANCHES, ROOM_TYPES, BRAND

class ImageGenerator:
    def __init__(self, use_pollinations=True):
        pass

    def generate(self, branch, room_type, theme, style="luxury"):
        prompt = self._build_prompt(branch, room_type, theme, style)
        _, fname = self._prepare_output()
        return self._generate_pollinations(prompt, fname)

    def _generate_pollinations(self, prompt, fname):
        try:
            url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1080&height=1350&nologo=true"
            resp = requests.get(url, timeout=90)
            resp.raise_for_status()
            fname.write_bytes(resp.content)
            print(f"[ImageGenerator] Pollinations ✅ → {fname}")
            return {"success": True, "file_path": str(fname), "source": "pollinations", "prompt": prompt}
        except Exception as e:
            print(f"[ImageGenerator] Error: {e}")
            return {"success": False, "error": str(e)}

    def _prepare_output(self):
        base = Path(__file__).parent.parent
        out_dir = base / "outputs" / datetime.now().strftime("%Y-%m")
        out_dir.mkdir(parents=True, exist_ok=True)
        fname = out_dir / f"{datetime.now().strftime('%d-%a').lower()}-poster.jpg"
        return out_dir, fname

    def _build_prompt(self, branch, room_type, theme, style):
        b = BRANCHES.get(branch, BRANCHES["gateway"])
        r = ROOM_TYPES.get(room_type, ROOM_TYPES["studio"])
        return (
            f"Instagram poster for {b['name']} Bandung apartment, theme {theme}. "
            f"{r['name']} room {r['size']}, {style} style, premium hospitality Indonesia, "
            f"clean modern layout, warm golden lighting, professional photography, "
            f"brand accent color {BRAND['primary_color']}, no watermark, no text overlay."
        )
