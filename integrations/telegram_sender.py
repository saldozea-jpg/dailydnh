import os
import requests

class TelegramSender:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def _validate(self):
        if not self.token: raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan.")
        if not self.chat_id: raise ValueError("TELEGRAM_CHAT_ID tidak ditemukan.")

    async def send_daily_report(self, report, poster):
        self._validate()
        theme = report.get("theme", {})
        trends = report.get("trends", {})
        caption_data = report.get("caption", {})
        hashtag_preview = " ".join(f"#{h['tag']}" for h in trends.get("hashtags", [])[:5])

        # Header report
        self.send_text(
            f"📅 <b>dailyDNH · {report.get('date','')} {report.get('time','')}</b>\n\n"
            f"🎯 <b>{theme.get('theme_name','')}</b>\n"
            f"🏨 {theme.get('branch','').replace('_',' ').title()} | 🛏 {theme.get('room_type','').upper()}\n"
            f"📌 {hashtag_preview}\n"
            f"{'' if caption_data.get('fallback') else '✅ Caption AI OK'}"
        )

        # Kirim prompt gambar (ganti send_photo)
        if poster and poster.get("success") and poster.get("prompt"):
            label = poster.get("context_label", "")
            copy_hint = poster.get("copy_suggestion", "")
            prompt = poster.get("prompt", "")
            self.send_text(
                f"🎨 <b>Prompt Poster Hari Ini</b>\n"
                f"{label}\n\n"
                f"<code>{prompt}</code>\n\n"
                f"💬 <i>{copy_hint}</i>\n\n"
                f"📋 Generate di:\n"
                f"• DALL-E → chat.openai.com\n"
                f"• Leonardo → app.leonardo.ai\n"
                f"• NanoBanana → nanobanana.com"
            )
        else:
            self.send_text("⚠️ Poster tidak tersedia hari ini.")

        # Caption siap pakai
        full_caption = caption_data.get("full_text", "")
        if full_caption:
            self.send_text(f"📋 <b>Caption siap pakai:</b>\n\n<code>{full_caption[:3500]}</code>")

        return True

    def send_text(self, message):
        self._validate()
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                data={"chat_id": self.chat_id, "text": message[:4096], "parse_mode": "HTML"},
                timeout=30
            )
            return True
        except Exception as e:
            print(f"[Telegram] Error teks: {e}"); return False