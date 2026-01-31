import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== TOKEN ==================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi. Render Environment Variables ni tekshir.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================== MENULAR ==================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        KeyboardButton("📊 Slayd"),
        KeyboardButton("📚 Referat / Mustaqil ish")
    )
    kb.row(
        KeyboardButton("🧩 Test tuzish"),
        KeyboardButton("🧩 Krossvord")
    )
    kb.row(
        KeyboardButton("💰 Balans"),
        KeyboardButton("🎁 Referal")
    )
    kb.row(
        KeyboardButton("ℹ️ Qo'llanma"),
        KeyboardButton("⚙️ Sozlamalar")
    )
    return kb


def language_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(
        KeyboardButton("🇺🇿 O'zbekcha"),
        KeyboardButton("🇷🇺 Русский")
    )
    return kb


# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 <b>Xush kelibsiz!</b>\n\n"
        "Avval tilni tanlang:",
        reply_markup=language_menu()
    )


# ================== LANGUAGE ==================
@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O'zbekcha", "🇷🇺 Русский"])
def set_language(message):
    if message.text == "🇺🇿 O'zbekcha":
        bot.send_message(
            message.chat.id,
            "✅ Til o'zbekcha qilindi.\nXizmatni tanlang:",
            reply_markup=main_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "✅ Язык установлен: русский.\nВыберите услугу:",
            reply_markup=main_menu()
        )


# ================== SERVICES ==================
@bot.message_handler(func=lambda m: m.text == "📊 Slayd")
def slide_service(message):
    bot.send_message(
        message.chat.id,
        "📊 <b>Slayd xizmati</b>\n\nMavzuni yuboring:"
    )


@bot.message_handler(func=lambda m: m.text == "📚 Referat / Mustaqil ish")
def referat_service(message):
    bot.send_message(
        message.chat.id,
        "📚 <b>Referat / Mustaqil ish</b>\n\nMavzuni aniq qilib yozing:"
    )


@bot.message_handler(func=lambda m: m.text == "🧩 Test tuzish")
def test_service(message):
    bot.send_message(
        message.chat.id,
        "🧩 <b>Test tuzish</b>\n\nMavzuni yuboring:"
    )


@bot.message_handler(func=lambda m: m.text == "🧩 Krossvord")
def crossword_service(message):
    bot.send_message(
        message.chat.id,
        "🧩 <b>Krossvord</b>\n\nMavzuni yuboring:"
    )


# ================== OTHER ==================
@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balance(message):
    bot.send_message(
        message.chat.id,
        "💰 Balans: <b>0 so'm</b>\n(Bonus va to'lov keyin qo'shiladi)",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda m: m.text == "🎁 Referal")
def referral(message):
    bot.send_message(
        message.chat.id,
        "🎁 Referal tizimi tez orada faollashadi.",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda m: m.text == "ℹ️ Qo'llanma")
def help_menu(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ <b>Qo'llanma</b>\n\n"
        "1️⃣ Xizmat tanlang\n"
        "2️⃣ Mavzuni yozing\n"
        "3️⃣ Natijani oling",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda m: m.text == "⚙️ Sozlamalar")
def settings(message):
    bot.send_message(
        message.chat.id,
        "⚙️ Sozlamalar hozircha mavjud emas.",
        reply_markup=main_menu()
    )


# ================== RUN ==================
print("Bot started successfully")
bot.infinity_polling()
