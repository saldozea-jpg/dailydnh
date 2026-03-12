#!/usr/bin/env python3
import os, sys, json, asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.image_generator import ImageGenerator
from generators.caption_generator import CaptionGenerator
from generators.trend_analyzer import TrendAnalyzer
from integrations.telegram_sender import TelegramSender

BASE_DIR = Path(__file__).parent.parent

async def main():
    branch   = os.getenv("MANUAL_BRANCH", "gateway")
    room_type = os.getenv("MANUAL_ROOM",  "studio")
    theme    = os.getenv("MANUAL_THEME",  "promo")
    style    = os.getenv("MANUAL_STYLE",  "luxury")
    print(f"🎬 Manual: {branch} / {room_type} / {theme} / {style}")

    now    = datetime.now()
    trends = TrendAnalyzer().get_trending(theme=theme)
    caption = CaptionGenerator().generate(theme=theme, branch=branch, room_type=room_type, tone="professional", trends=trends)
    poster  = ImageGenerator().generate(branch=branch, room_type=room_type, theme=theme, style=style)

    report = {"date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M"), "theme": {"theme_name": f"Manual: {theme}", "branch": branch, "room_type": room_type, "tone": "professional"}, "trends": trends, "caption": caption}

    d = BASE_DIR / "outputs" / now.strftime("%Y-%m")
    d.mkdir(parents=True, exist_ok=True)
    (d / f"manual-{now.strftime('%d-%H%M')}-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    await TelegramSender().send_daily_report(report, poster)
    print("✅ Manual selesai!")

if __name__ == "__main__":
    asyncio.run(main())
