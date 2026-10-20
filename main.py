import logging
import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests
from bs4 import BeautifulSoup

# Logging ayarları
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# 1. Flask mini-sunucusu (Render port isteği için şarttır)
app_web = Flask(__name__)


@app_web.route("/")
def home():
    return "Aura Bot Aktif ve Çalışıyor!", 200


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


# 2. Telegram Bot Komutları
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aura Bot başarıyla aktif edildi ve çalışıyor efendim!"
    )


async def durum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Aura Bot sorunsuz çalışıyor ve arka planda aktif efendim!"
    )


async def tara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Anlık tarama başlatılıyor efendim...")
    try:
        # Örnek haber/R10 akış kontrolü
        url = "https://news.google.com/rss"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "xml")
        item = soup.find("item")
        
        if item:
            title = item.title.text
            link = item.link.text
            msg = f"🔔 **Aura Ajans Anlık Tarama Sonucu:**\n\n📌 {title}\n\n🔗 {link}"
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("Şu an yeni bir sonuç bulunamadı efendim.")
    except Exception as e:
        await update.message.reply_text(f"Tarama sırasında bir hata oluştu efendim: {e}")


def main():
    # Doğru ve güncel Telegram Bot Token'ınız:
    TOKEN = "8851902854:AAFygSpAFQ_4w8w2V851CDrp5A9yOvVGdJY"

    # Telegram Bot uygulamasını başlatıyoruz
    application = ApplicationBuilder().token(TOKEN).build()

    # Komut bağlamaları
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("durum", durum))
    application.add_handler(CommandHandler("tara", tara))

    print("Aura Bot Başlatıldı...")
    application.run_polling()


if __name__ == "__main__":
    import threading

    # Flask sunucusunu arka planda çalıştırıyoruz
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

    # Telegram botunu ana akışta çalıştırıyoruz
    main()
