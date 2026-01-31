Bekzod, [01.02.2026 0:35]
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== CONFIG ==================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================== CONSTANTS ==================
SERVICES = {
    "presentation": "📕 Taqdimot",
    "referat": "📘 Referat / Mustaqil ish",
    "essay": "✍️ Esse",
    "course": "📚 Kurs ishi",
    "bmi": "🎓 BMI"
}

LANGUAGES = ["🇺🇿 O‘zbek", "🇷🇺 Русский", "🇬🇧 English"]

PRICES = {
    "presentation": 5000,
    "referat": 7000,
    "essay": 6000,
    "course": 15000,
    "bmi": 20000
}

# ================== USER STATE (FSM) ==================
STATE_NONE = "none"
STATE_TOPIC = "topic"
STATE_SIZE = "size"
STATE_LANGUAGE = "language"

user_state = {}
user_data = {}

def reset_user(user_id):
    user_state[user_id] = STATE_NONE
    user_data[user_id] = {
        "service": None,
        "topic": None,
        "size": None,
        "language": None
    }

# ================== KEYBOARDS ==================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📕 Taqdimot", "📘 Referat / Mustaqil ish")
    kb.row("✍️ Esse", "📚 Kurs ishi", "🎓 BMI")
    kb.row("👑 VIP", "💰 Balans", "🎁 Referal")
    kb.row("⚙️ Sozlamalar")
    return kb

def back_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("⬅️ Ortga")
    return kb

def size_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("5", "10", "15")
    kb.row("20", "30")
    kb.add("⬅️ Ortga")
    return kb

def language_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for l in LANGUAGES:
        kb.add(l)
    kb.add("⬅️ Ortga")
    return kb

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    reset_user(user_id)

    bot.send_message(
        message.chat.id,
        "👋 <b>Xush kelibsiz!</b>\n\n"
        "Biz AI yordamida <b>taqdimot, referat, esse, kurs ishi va BMI</b> tayyorlaymiz.\n\n"
        "👇 Kerakli xizmatni tanlang:",
        reply_markup=main_menu()
    )

# ================== SERVICE SELECTION ==================
@bot.message_handler(func=lambda m: m.text in SERVICES.values())
def select_service(message):
    user_id = message.from_user.id

    for key, name in SERVICES.items():
        if message.text == name:
            user_data[user_id]["service"] = key
            break

    user_state[user_id] = STATE_TOPIC

    bot.send_message(
        message.chat.id,
        f"📌 <b>{message.text}</b>\n\n"
        "Mavzuni to‘liq va aniq yozing:",
        reply_markup=back_kb()
    )

# ================== TOPIC ==================
@bot.message_handler(func=lambda m: user_state.get(m.from_user.id) == STATE_TOPIC)
def get_topic(message):
    user_id = message.from_user.id

    if message.text == "⬅️ Ortga":
        start(message)
        return

    user_data[user_id]["topic"] = message.text
    user_state[user_id] = STATE_SIZE

    bot.send_message(
        message.chat.id,
        "📄 Ish hajmini tanlang (bet/slayd):",
        reply_markup=size_kb()
    )

# ================== SIZE ==================
@bot.message_handler(func=lambda m: user_state.get(m.from_user.id) == STATE_SIZE)
def get_size(message):
    user_id = message.from_user.id

    if message.text == "⬅️ Ortga":
        user_state[user_id] = STATE_TOPIC
        bot.send_message(message.chat.id, "📌 Mavzuni qayta yozing:", reply_markup=back_kb())
        return

    if not message.text.isdigit():
        bot.send_message(message.chat.id, "❗ Iltimos, faqat raqam tanlang.", reply_markup=size_kb())
        return

    user_data[user_id]["size"] = int(message.text)
    user_state[user_id] = STATE_LANGUAGE

    bot.send_message(
        message.chat.id,
        "🌐 Qaysi tilda tayyorlaymiz?",
        reply_markup=language_kb()
    )

Bekzod, [01.02.2026 0:35]
# ================== LANGUAGE ==================
@bot.message_handler(func=lambda m: user_state.get(m.from_user.id) == STATE_LANGUAGE)
def get_language(message):
    user_id = message.from_user.id

    if message.text == "⬅️ Ortga":
        user_state[user_id] = STATE_SIZE
        bot.send_message(message.chat.id, "📄 Hajmni tanlang:", reply_markup=size_kb())
        return

    if message.text not in LANGUAGES:
        bot.send_message(message.chat.id, "❗ Tilni tugmalar orqali tanlang.", reply_markup=language_kb())
        return

    user_data[user_id]["language"] = message.text
    service = user_data[user_id]["service"]
    price = PRICES[service]

    bot.send_message(
        message.chat.id,
        "✅ <b>Buyurtma qabul qilindi</b>\n\n"
        f"📌 Xizmat: {SERVICES[service]}\n"
        f"📝 Mavzu: {user_data[user_id]['topic']}\n"
        f"📄 Hajm: {user_data[user_id]['size']}\n"
        f"🌐 Til: {user_data[user_id]['language']}\n\n"
        f"💰 Narx: <b>{price} so‘m</b>\n\n"
        "Keyingi bosqichda to‘lov va fayl avtomatik yaratiladi.",
        reply_markup=main_menu()
    )

    reset_user(user_id)

# ================== OTHER ==================
@bot.message_handler(func=lambda m: m.text in ["👑 VIP", "💰 Balans", "🎁 Referal", "⚙️ Sozlamalar"])
def other(message):
    bot.send_message(
        message.chat.id,
        "🔧 Ushbu bo‘lim hozir ishlab chiqilmoqda.\n"
        "Asosiy xizmatlar to‘liq ishlayapti.",
        reply_markup=main_menu()
    )

# ================== RUN ==================
print("Bot started (PRO)")
bot.infinity_polling()
