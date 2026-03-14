"""
DNH Property — AI Laporan Harian SaldoZea
Jadwal: 08:30 WIB setiap hari
Kirim via: Telegram + Email
"""

import os
import json
import requests
import smtplib
import traceback
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from groq import Groq

# ─── timezone WIB ─────────────────────────────────────────────────────────────
WIB = timezone(timedelta(hours=7))
now = datetime.now(WIB)
today_str = now.strftime("%A, %d %B %Y")
today_key = now.strftime("%Y-%m-%d")
yesterday_key = (now - timedelta(days=1)).strftime("%Y-%m-%d")

# ─── env ──────────────────────────────────────────────────────────────────────
FIREBASE_URL   = os.environ["FIREBASE_URL"]
FIREBASE_TOKEN = os.environ.get("FIREBASE_TOKEN", "")
GROQ_API_KEY   = os.environ["GROQ_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT  = os.environ["TELEGRAM_CHAT_ID"]
GMAIL_USER     = os.environ.get("GMAIL_USER", "")
GMAIL_PASS     = os.environ.get("GMAIL_APP_PASSWORD", "")
EMAIL_TO       = os.environ.get("EMAIL_TO", GMAIL_USER)


# ─── ambil data firebase ──────────────────────────────────────────────────────
def fetch_firebase(path: str) -> dict:
    url = f"{FIREBASE_URL}/{path}.json"
    params = {}
    if FIREBASE_TOKEN:
        params["auth"] = FIREBASE_TOKEN
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json() or {}


def get_saldozea_data() -> dict:
    data = {}
    nodes_to_fetch = [
        "transactions", "bookings", "rooms", "revenue",
        "units", "payments", "reservations", "saldo",
        "history", "pemasukan", "pengeluaran", "kamar",
    ]
    for node in nodes_to_fetch:
        try:
            result = fetch_firebase(node)
            if result:
                data[node] = result
        except Exception:
            pass
    if not data:
        try:
            data = fetch_firebase("")
        except Exception as e:
            data = {"error": str(e)}
    return data


# ─── ringkas data ─────────────────────────────────────────────────────────────
def summarize_data(raw: dict, max_entries: int = 80) -> str:
    summary_parts = []
    total_entries = 0

    def extract(obj, prefix="", depth=0):
        nonlocal total_entries
        if depth > 4 or total_entries >= max_entries:
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                extract(v, f"{prefix}/{k}" if prefix else k, depth + 1)
        elif isinstance(obj, list):
            for i, v in enumerate(obj[:10]):
                extract(v, f"{prefix}[{i}]", depth + 1)
        else:
            summary_parts.append(f"{prefix}: {str(obj)[:120]}")
            total_entries += 1

    extract(raw)
    if not summary_parts:
        return "Tidak ada data tersedia dari Firebase."
    return "\n".join(summary_parts)


# ─── generate laporan via Groq ────────────────────────────────────────────────
def generate_report(data_summary: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = """Kamu adalah asisten bisnis senior untuk DNH Property, 
sebuah bisnis penyewaan apartemen di Bandung dengan tiga cabang: 
Gateway Pasteur (utama), Jarrdin Cihampelas, dan Grand Asia Afrika.

Tugasmu: buat laporan harian yang rinci, terstruktur, dan actionable 
berdasarkan data Firebase SaldoZea yang diberikan.

Format laporan WAJIB menggunakan struktur ini:

📊 LAPORAN HARIAN DNH PROPERTY
[tanggal hari ini]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 RINGKASAN KEUANGAN
[total pendapatan, pengeluaran, net profit jika ada datanya]

🏠 OCCUPANCY & BOOKING
[data per cabang: Gateway Pasteur, Jarrdin, Grand Asia Afrika]

📈 TRANSAKSI HARI INI
[daftar transaksi atau booking terbaru yang relevan]

⚠️ PERHATIAN KHUSUS
[anomali, pembayaran pending, unit bermasalah, hal yang perlu ditindaklanjuti]

📋 REKOMENDASI HARI INI
[3-5 aksi konkret yang bisa dilakukan Beje hari ini]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Laporan otomatis DNH Property | dailyDNH sistem

Aturan:
- Gunakan bahasa Indonesia yang natural dan profesional
- Jika data tidak ada untuk suatu bagian, tulis: Data tidak tersedia
- Tampilkan angka dalam format Rupiah (Rp xxx.xxx)
- Jangan mengarang data, hanya analisis dari data yang tersedia
- Jadikan laporan ini benar-benar berguna untuk pengambilan keputusan bisnis"""

    user_prompt = f"""Hari ini: {today_str}

Data SaldoZea dari Firebase:
---
{data_summary}
---

Buat laporan harian yang lengkap dan actionable berdasarkan data di atas."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=2000,
    )
    return response.choices[0].message.content.strip()


# ─── kirim telegram ───────────────────────────────────────────────────────────
def send_telegram(report_md: str) -> bool:
    def send_chunk(text: str) -> bool:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }
        resp = requests.post(url, json=payload, timeout=15)
        return resp.status_code == 200

    max_len = 4000
    if len(report_md) <= max_len:
        return send_chunk(report_md)

    parts = []
    current = ""
    for line in report_md.split("\n"):
        if len(current) + len(line) + 1 > max_len:
            parts.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        parts.append(current)

    success = True
    for i, part in enumerate(parts, 1):
        header = f"*[{i}/{len(parts)}]*\n" if len(parts) > 1 else ""
        if not send_chunk(header + part):
            success = False
    return success


# ─── kirim email ─────────────────────────────────────────────────────────────
def markdown_to_html(md: str) -> str:
    import re
    lines = md.split("\n")
    html_lines = []
    for line in lines:
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
        if line.startswith("# "):
            line = f"<h1>{line[2:]}</h1>"
        elif line.startswith("## "):
            line = f"<h2>{line[3:]}</h2>"
        elif line.startswith("### "):
            line = f"<h3>{line[4:]}</h3>"
        elif line.startswith("---"):
            line = "<hr>"
        elif line.strip() == "":
            line = "<br>"
        else:
            line = f"<p>{line}</p>"
        html_lines.append(line)
    return "\n".join(html_lines)


def send_email(report_md: str) -> bool:
    if not GMAIL_USER or not GMAIL_PASS:
        print("Email dilewati: GMAIL_USER atau GMAIL_APP_PASSWORD tidak diset.")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📊 Laporan Harian DNH Property — {now.strftime('%d %b %Y')}"
        msg["From"] = f"DNH Property Report <{GMAIL_USER}>"
        msg["To"] = EMAIL_TO

        html_body = f"""
        <html><body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 700px; 
            margin: 0 auto; padding: 20px; color: #1a1a2e; background: #f8f9fa;">
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
                color: white; padding: 24px 32px; border-radius: 12px 12px 0 0;">
                <h1 style="margin:0; font-size:22px;">📊 Laporan Harian DNH Property</h1>
                <p style="margin:6px 0 0; opacity:0.8; font-size:14px;">{today_str}</p>
            </div>
            <div style="background: white; padding: 28px 32px; 
                border: 1px solid #e0e0e0; border-radius: 0 0 12px 12px;">
                {markdown_to_html(report_md)}
            </div>
            <p style="text-align:center; font-size:11px; color:#888; margin-top:16px;">
                Dikirim otomatis oleh dailyDNH sistem · DNH Property Bandung
            </p>
        </body></html>
        """

        msg.attach(MIMEText(report_md, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, EMAIL_TO, msg.as_string())
        return True
    except Exception as e:
        print(f"Gagal kirim email: {e}")
        return False


# ─── notif error ──────────────────────────────────────────────────────────────
def notify_error(error_msg: str):
    text = f"❌ *Laporan Harian Gagal*\n\n```\n{error_msg[:500]}\n```\n\n_{today_str}_"
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT, "text": text, "parse_mode": "Markdown"},
            timeout=10,
        )
    except Exception:
        pass


# ─── main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"[{now.strftime('%H:%M:%S WIB')}] Mulai generate laporan harian...")
    try:
        print("→ Mengambil data dari Firebase SaldoZea...")
        raw_data = get_saldozea_data()
        data_summary = summarize_data(raw_data)
        print(f"→ Data diambil: {len(data_summary)} karakter")

        print("→ Generating laporan dengan Groq AI...")
        report = generate_report(data_summary)
        print(f"→ Laporan selesai: {len(report)} karakter")

        print("→ Mengirim ke Telegram...")
        tg_ok = send_telegram(report)
        print(f"→ Telegram: {'berhasil' if tg_ok else 'gagal'}")

        print("→ Mengirim ke Email...")
        email_ok = send_email(report)
        print(f"→ Email: {'berhasil' if email_ok else 'dilewati/gagal'}")

        if not tg_ok and not email_ok:
            raise Exception("Semua channel pengiriman gagal.")

        print("Laporan harian berhasil dikirim!")
    except Exception as e:
        err = traceback.format_exc()
        print(f"Error: {e}\n{err}")
        notify_error(str(e))
        raise


if __name__ == "__main__":
    main()
