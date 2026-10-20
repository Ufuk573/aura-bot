from flask import Flask
import threading
import logging
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Render'ın Web Servis Port İstediğini Karşılayan Mini Sunucu
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Aura Bot Aktif ve Çalışıyor!"

def run_web():
    app_web.run(host='0.0.0.0', port=10000)

# Web sunucusunu arka planda başlatıyoruz
threading.Thread(target=run_web).daemon = True

# Telegram Ayarları
BOT_TOKEN = "8851902854:AAGsO0N2g_Jd8BIsG2d-qDThfX23jA4d9E4"
CHAT_ID = "6899627812"

# Logging Ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# R10 Tarama Fonksiyonu
async def r10_tara():
    url = "https://www.r10.net/yeni-konular/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            konular = soup.find_all('a', class_='topic-title', limit=5)
            sonuc = []
            for k in konular:
                baslik = k.text.strip()
                link = "https://www.r10.net" + k['href'] if k['href'].startswith('/') else k['href']
                sonuc.append(f"📌 **{baslik}**\n🔗 {link}")
            return "\n\n".join(sonuc) if sonuc else "Yeni konu bulunamadı veya yapı değişti."
        else:
            return f"R10'a ulaşılamadı. Durum Kodu: {response.status_code}"
    except Exception as e:
        return f"Tarama sırasında hata oluştu: {str(e)}"

# Komutlar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aura Bot 7/24 Bulut Sunucusunda Aktif! 🚀\n\nKomutlar:\n/tara - R10 Yeni Konuları Tara\n/durum - Bot Durumu")

async def durum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Aura Bot Render.com üzerinde 7/24 kesintisiz çalışıyor!")

async def tara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 R10 taranıyor, lütfen bekleyin...")
    mesaj = await r10_tara()
    await update.message.reply_text(mesaj, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("durum", durum))
    app.add_handler(CommandHandler("tara", tara))
    
    print("Aura Bot Başlatıldı...")
    app.run_polling()
