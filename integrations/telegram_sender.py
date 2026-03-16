import os
import requests

class TelegramSender:
    def __init__(self):
        self.token   = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def _validate(self):
        if not self.token:   raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan.")
        if not self.chat_id: raise ValueError("TELEGRAM_CHAT_ID tidak ditemukan.")

    async def send_daily_report(self, report, poster):
        self._validate()
        theme        = report.get("theme", {})
        trends       = report.get("trends", {})
        caption_data = report.get("caption", {})
        hashtag_preview = " ".join(f"#{h['tag']}" for h in trends.get("hashtags", [])[:5])
        full_caption    = caption_data.get("full_text", "")

        # ── 1. Header singkat ────────────────────────────────────────────────
        self.send_text(
            f"📅 <b>dailyDNH · {report.get('date','')} {report.get('time','')}</b>\n\n"
            f"🎯 <b>{theme.get('theme_name','')}</b>\n"
            f"🏨 {theme.get('branch','').replace('_',' ').title()} | "
            f"🛏 {theme.get('room_type','').upper()}\n"
            f"📌 {hashtag_preview}\n"
            f"{'✅ Caption AI OK' if not caption_data.get('fallback') else '⚠️ Caption fallback'}"
        )

        # ── 2. Kirim poster gambar ───────────────────────────────────────────
        if poster and poster.get("success"):
            image_path = poster.get("image_path")

            if image_path:
                # Gambar berhasil digenerate → kirim langsung
                label = poster.get("context_label", "")
                photo_caption = (
                    f"{label}\n\n"
                    f"{'✂️ ' + full_caption[:800] if full_caption else ''}"
                )
                ok = self.send_photo(image_path, caption=photo_caption)

                if ok:
                    print("[Telegram] Poster gambar terkirim ✅")
                else:
                    print("[Telegram] Gagal kirim foto, fallback ke prompt teks")
                    self._send_prompt_fallback(poster)

                # Hapus file temp
                try:
                    os.unlink(image_path)
                except Exception:
                    pass
            else:
                # Pollinations gagal → kirim prompt teks saja
                self._send_prompt_fallback(poster)
        else:
            self.send_text("⚠️ Poster tidak tersedia hari ini.")

        # ── 3. Caption lengkap siap pakai ────────────────────────────────────
        if full_caption:
            self.send_text(
                f"📋 <b>Caption siap pakai:</b>\n\n"
                f"<code>{full_caption[:3500]}</code>"
            )

        return True

    # ── Helpers ──────────────────────────────────────────────────────────────

    def send_photo(self, image_path: str, caption: str = "") -> bool:
        """Kirim foto dari file lokal ke Telegram."""
        self._validate()
        try:
            with open(image_path, "rb") as f:
                resp = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendPhoto",
                    data={
                        "chat_id":    self.chat_id,
                        "caption":    caption[:1024],
                        "parse_mode": "HTML",
                    },
                    files={"photo": f},
                    timeout=60,
                )
            if resp.status_code != 200:
                print(f"[Telegram] sendPhoto error {resp.status_code}: {resp.text[:200]}")
            return resp.status_code == 200
        except Exception as e:
            print(f"[Telegram] Error foto: {e}")
            return False

    def send_text(self, message: str) -> bool:
        """Kirim pesan teks ke Telegram."""
        self._validate()
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                data={
                    "chat_id":    self.chat_id,
                    "text":       message[:4096],
                    "parse_mode": "HTML",
                },
                timeout=30,
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"[Telegram] Error teks: {e}")
            return False

    def _send_prompt_fallback(self, poster: dict):
        """Fallback: kirim prompt teks jika gambar gagal digenerate."""
        prompt      = poster.get("prompt", "")
        label       = poster.get("context_label", "")
        copy_hint   = "Salin prompt → generate di Leonardo AI / DALL-E 3 / Midjourney"
        self.send_text(
            f"🎨 <b>Prompt Poster (gambar gagal digenerate)</b>\n"
            f"{label}\n\n"
            f"<code>{prompt}</code>\n\n"
            f"💬 <i>{copy_hint}</i>"
        )
