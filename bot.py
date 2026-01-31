import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== TOKEN ==================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi. Render -> Environment Variables ni tekshir.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================== MAIN MENU ==================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        KeyboardButton("📘 Taqdimot"),
        KeyboardButton("📚 Referat / Mustaqil ish")
    )
    kb.row(
        KeyboardButton("💰 Balans"),
        KeyboardButton("🎁 Referal")
    )
    kb.row(
        KeyboardButton("👑 VIP Status"),
        KeyboardButton("ℹ️ Qo'llanma")
    )
    return kb

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 <b>Xush kelibsiz!</b>\n\n"
        "Bu bot orqali:\n"
        "📘 Taqdimot\n"
        "📚 Referat / Mustaqil ish\n"
        "🧠 AI xizmatlardan foydalanishingiz mumkin.",
        reply_markup=main_menu()
    )

# ================== SERVICES ==================
@bot.message_handler(func=lambda m: m.text == "📘 Taqdimot")
def taqdimot(message):
    bot.send_message(
        message.chat.id,
        "📘 <b>Taqdimot xizmati</b>\n\n"
        "Mavzuni yozing, keyingi bosqichlarda hajm va til tanlanadi.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "📚 Referat / Mustaqil ish")
def referat(message):
    bot.send_message(
        message.chat.id,
        "📚 <b>Referat / Mustaqil ish</b>\n\n"
        "Mavzuni to‘liq va aniq yozib yuboring.",
        reply_markup=main_menu()
    )

# ================== OTHER ==================
@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balans(message):
    bot.send_message(
        message.chat.id,
        "💰 <b>Balans</b>\n\nHozircha test rejimida.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🎁 Referal")
def referal(message):
    bot.send_message(
        message.chat.id,
        "🎁 <b>Referal tizimi</b>\n\nTez orada faollashtiriladi.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "👑 VIP Status")
def vip(message):
    bot.send_message(
        message.chat.id,
        "👑 <b>VIP Status</b>\n\nCheksiz foydalanish tez orada.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "ℹ️ Qo'llanma")
def help_menu(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ <b>Qo‘llanma</b>\n\n"
        "1️⃣ Xizmat tanlang\n"
        "2️⃣ Mavzuni yozing\n"
        "3️⃣ Natijani oling",
        reply_markup=main_menu()
    )

# ================== RUN ==================
print("Bot started (PRO)")
bot.infinity_polling(skip_pending=True)
