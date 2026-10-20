import logging
import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

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


def main():
    # Token'ınız loglardaki ekrandan alınarak buraya entegre edilmiştir efendim:
    TOKEN = "8851902854:AAGsO0N2g_Jd8BlSG2d-qDThfX23jA4d9E4"

    # Telegram Bot uygulamasını başlatıyoruz
    application = ApplicationBuilder().token(TOKEN).build()

    # Komut bağlamaları
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("durum", durum))

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
