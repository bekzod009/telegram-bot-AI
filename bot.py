import os
import telebot

# =========================
# ENVIRONMENT TOKEN
# =========================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "❌ BOT_TOKEN topilmadi. Render → Environment Variables ni tekshir."
    )

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# =========================
# /start
# =========================
@bot.message_handler(commands=["start"])
def start_handler(message):
    text = (
        "🤖 <b>AI Taqdimot Bot</b>\n\n"
        "Xush kelibsiz!\n"
        "Bu bot orqali:\n"
        "• Slayd tayyorlash\n"
        "• PDF yaratish\n"
        "• Buyurtmalar berish\n\n"
        "Davom etish uchun menyudan tanlang 👇"
    )
    bot.send_message(message.chat.id, text)

# =========================
# TEST /ping (server tirikmi)
# =========================
@bot.message_handler(commands=["ping"])
def ping(message):
    bot.send_message(message.chat.id, "✅ Bot ishlayapti")

# =========================
# UNKNOWN MESSAGE
# =========================
@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(
        message.chat.id,
        "⚠️ Buyruq tushunilmadi.\n/start ni bosing."
    )

# =========================
# START BOT
# =========================
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)
