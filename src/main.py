#!/usr/bin/env python3
import os, sys, json, asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.image_generator import ImageGenerator
from generators.caption_generator import CaptionGenerator
from generators.trend_analyzer import TrendAnalyzer
from integrations.telegram_sender import TelegramSender
from config.weekly_themes import get_today_theme

BASE_DIR = Path(__file__).parent.parent

async def main_async():
    now = datetime.now()
    print(f"🚀 dailyDNH starting... {now.strftime('%Y-%m-%d %H:%M')} WIB")
    try:
        theme_data = get_today_theme()
        print(f"📅 {theme_data['day_name']} → {theme_data['theme_name']}")
    except Exception as e:
        print(f"❌ Theme error: {e}"); return 1

    try:
        trends = TrendAnalyzer().get_trending(theme=theme_data["theme"])
    except Exception as e:
        print(f"⚠️ Trend error: {e}"); trends = {"hashtags": [], "audio": []}

    try:
        caption = CaptionGenerator().generate(theme=theme_data["theme"], branch=theme_data["branch"], room_type=theme_data["room_type"], tone=theme_data["tone"], trends=trends)
    except Exception as e:
        print(f"⚠️ Caption error: {e}"); caption = {"full_text": "[Caption failed]", "hashtags": [], "fallback": True}

    try:
        poster = ImageGenerator().generate(branch=theme_data["branch"], room_type=theme_data["room_type"], theme=theme_data["theme"], style=theme_data.get("style", "luxury"))
    except Exception as e:
        print(f"⚠️ Poster error: {e}"); poster = {"success": False, "error": str(e)}

    report = {"date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M"), "theme": theme_data, "trends": trends, "caption": caption}
    d = BASE_DIR / "outputs" / now.strftime("%Y-%m")
    d.mkdir(parents=True, exist_ok=True)
    day = now.strftime("%d-%a").lower()
    (d / f"{day}-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / f"{day}-caption.txt").write_text(caption.get("full_text", ""), encoding="utf-8")

    await TelegramSender().send_daily_report(report, poster)
    print("✅ Selesai!")
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main_async()))
