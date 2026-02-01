Bekzod, [02.02.2026 1:05]
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi. Render Environment ni tekshir.")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ================== STATES ==================
STATE_NONE = "NONE"
STATE_TOPIC = "TOPIC"

user_state = {}
user_data = {}

# ================== KEYBOARDS ==================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📊 Slayd"),
        KeyboardButton("📚 Referat / Mustaqil ish"),
    )
    kb.add(
        KeyboardButton("🧪 Test tuzish"),
        KeyboardButton("🧩 Krossvord"),
    )
    kb.add(
        KeyboardButton("💰 Balans"),
        KeyboardButton("🎁 Referal"),
    )
    kb.add(KeyboardButton("ℹ️ Qo'llanma"))
    return kb

# ================== HELPERS ==================
def set_state(user_id, state):
    user_state[user_id] = state

def get_state(user_id):
    return user_state.get(user_id, STATE_NONE)

def reset_user(user_id):
    user_state[user_id] = STATE_NONE
    user_data.pop(user_id, None)

# ================== COMMANDS ==================
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    reset_user(user_id)

    bot.send_message(
        message.chat.id,
        "👋 <b>Assalomu alaykum!</b>\n\n"
        "Quyidagi xizmatlardan birini tanlang:",
        reply_markup=main_menu()
    )

# ================== SERVICES ==================
@bot.message_handler(func=lambda m: m.text == "📊 Slayd")
def slayd_service(message):
    user_id = message.from_user.id
    user_data[user_id] = {"service": "slayd"}
    set_state(user_id, STATE_TOPIC)

    bot.send_message(
        message.chat.id,
        "📊 <b>Slayd xizmati</b>\n\n"
        "Mavzuni to‘liq va aniq yozing:"
    )

@bot.message_handler(func=lambda m: m.text == "📚 Referat / Mustaqil ish")
def referat_service(message):
    user_id = message.from_user.id
    user_data[user_id] = {"service": "referat"}
    set_state(user_id, STATE_TOPIC)

    bot.send_message(
        message.chat.id,
        "📚 <b>Referat / Mustaqil ish</b>\n\n"
        "Mavzuni to‘liq va aniq yozing:"
    )

@bot.message_handler(func=lambda m: m.text == "🧪 Test tuzish")
def test_service(message):
    bot.send_message(
        message.chat.id,
        "🧪 Test tuzish xizmati\n\nTez orada ishga tushadi.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🧩 Krossvord")
def crossword_service(message):
    bot.send_message(
        message.chat.id,
        "🧩 Krossvord yaratish\n\nTez orada ishga tushadi.",
        reply_markup=main_menu()
    )

# ================== INFO ==================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Qo'llanma")
def help_menu(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ <b>Qo'llanma</b>\n\n"
        "1️⃣ Xizmat tanlang\n"
        "2️⃣ Mavzu yozing\n"
        "3️⃣ Natijani oling",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balance(message):
    bot.send_message(
        message.chat.id,
        "💰 Balans: <b>0 so'm</b>\n\n(To‘lovlar keyin ulanadi)",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🎁 Referal")
def referral(message):
    bot.send_message(
        message.chat.id,
        "🎁 Referal tizimi\n\nTez orada faollashadi.",
        reply_markup=main_menu()
    )

# ================== TOPIC HANDLER ==================
@bot.message_handler(func=lambda m: get_state(m.from_user.id) == STATE_TOPIC)
def handle_topic(message):
    user_id = message.from_user.id
    topic = message.text.strip()

    if len(topic) < 5:
        bot.send_message(message.chat.id, "❗️ Mavzu juda qisqa. Qayta yozing:")
        return

    service = user_data[user_id]["service"]

Bekzod, [02.02.2026 1:05]
bot.send_message(
        message.chat.id,
        "✅ <b>Mavzu qabul qilindi!</b>\n\n"
        f"🛠 Xizmat: <b>{service}</b>\n"
        f"📌 Mavzu: <b>{topic}</b>\n\n"
        "Keyingi bosqichlar tez orada qo‘shiladi.",
        reply_markup=main_menu()
    )

    reset_user(user_id)

# ================== FALLBACK ==================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "❗️ Iltimos, menyudan foydalaning.",
        reply_markup=main_menu()
    )

# ================== RUN ==================
print("Bot started (PRO)")
bot.infinity_polling(skip_pending=True)
