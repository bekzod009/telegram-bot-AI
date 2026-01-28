import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# =========================
# TOKEN (ENV)
# =========================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "❌ BOT_TOKEN topilmadi. Render → Environment Variables ni tekshir."
    )

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# =========================
# MAIN MENU
# =========================
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(
        KeyboardButton("📑 Taqdimot"),
        KeyboardButton("📄 Referat")
    )

    markup.row(
        KeyboardButton("📝 Mustaqil ish"),
        KeyboardButton("🎓 Kurs ishi")
    )

    markup.row(
        KeyboardButton("💰 Balans"),
        KeyboardButton("📜 Buyurtmalar tarixi")
    )

    return markup

# =========================
# /START
# =========================
@bot.message_handler(commands=["start"])
def start_handler(message):
    text = (
        "🚀 <b>Talabalar uchun AI yordamchi</b>\n\n"
        "Vaqtingizni tejang — ishni biz qilamiz.\n\n"
        "📑 Taqdimot\n"
        "📄 Referat\n"
        "📝 Mustaqil ish\n"
        "🎓 Kurs ishi\n\n"
        "Buyurtma berish uchun pastdagi menyudan tanlang 👇"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )

# =========================
# MENU HANDLERS
# =========================
@bot.message_handler(func=lambda m: m.text == "📑 Taqdimot")
def presentation(message):
    bot.send_message(
        message.chat.id,
        "📑 <b>Taqdimot</b>\n\n"
        "Slayd tayyorlash xizmati.\n"
        "Tez orada buyurtma berish mumkin bo‘ladi."
    )

@bot.message_handler(func=lambda m: m.text == "📄 Referat")
def referat(message):
    bot.send_message(
        message.chat.id,
        "📄 <b>Referat</b>\n\n"
        "Referat va ilmiy ishlar tayyorlash xizmati.\n"
        "Tez orada buyurtma berish mumkin bo‘ladi."
    )

@bot.message_handler(func=lambda m: m.text == "📝 Mustaqil ish")
def mustaqil_ish(message):
    bot.send_message(
        message.chat.id,
        "📝 <b>Mustaqil ish</b>\n\n"
        "Mustaqil ishlar tayyorlash xizmati.\n"
        "Tez orada buyurtma berish mumkin bo‘ladi."
    )

@bot.message_handler(func=lambda m: m.text == "🎓 Kurs ishi")
def kurs_ishi(message):
    bot.send_message(
        message.chat.id,
        "🎓 <b>Kurs ishi</b>\n\n"
        "Kurs ishi buyurtma qilish xizmati.\n"
        "Tez orada buyurtma berish mumkin bo‘ladi."
    )

@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balance(message):
    bot.send_message(
        message.chat.id,
        "💰 <b>Balans</b>\n\n"
        "Balansingiz: 0 so‘m\n"
        "To‘lov funksiyasi tez orada qo‘shiladi."
    )

@bot.message_handler(func=lambda m: m.text == "📜 Buyurtmalar tarixi")
def history(message):
    bot.send_message(
        message.chat.id,
        "📜 <b>Buyurtmalar tarixi</b>\n\n"
        "Hozircha buyurtmalar mavjud emas."
    )

# =========================
# /PING
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
