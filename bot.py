Bekzod, [02.02.2026 1:13]
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== TOKEN ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None or BOT_TOKEN.strip() == "":
    raise RuntimeError("BOT_TOKEN topilmadi. Render → Environment Variables ni tekshir.")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ================== USER STATE ==================
STATE_NONE = "NONE"
STATE_WAIT_TOPIC = "WAIT_TOPIC"

user_state = {}
user_data = {}

def set_state(user_id, state):
    user_state[user_id] = state

def get_state(user_id):
    return user_state.get(user_id, STATE_NONE)

def reset_user(user_id):
    user_state[user_id] = STATE_NONE
    user_data.pop(user_id, None)

# ================== KEYBOARDS ==================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📊 Slayd"))
    kb.add(KeyboardButton("📚 Referat / Mustaqil ish"))
    kb.add(KeyboardButton("🧪 Test"))
    kb.add(KeyboardButton("🧩 Krossvord"))
    kb.add(KeyboardButton("💰 Balans"))
    kb.add(KeyboardButton("ℹ️ Qo'llanma"))
    return kb

# ================== START ==================
@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.from_user.id
    reset_user(user_id)

    bot.send_message(
        message.chat.id,
        "👋 <b>Xush kelibsiz!</b>\n\n"
        "Quyidagi xizmatlardan birini tanlang:",
        reply_markup=main_menu()
    )

# ================== SERVICES ==================
@bot.message_handler(func=lambda m: m.text == "📊 Slayd")
def slayd_handler(message):
    user_id = message.from_user.id
    user_data[user_id] = {"service": "Slayd"}
    set_state(user_id, STATE_WAIT_TOPIC)

    bot.send_message(
        message.chat.id,
        "📊 <b>Slayd xizmati</b>\n\n"
        "✍️ Iltimos, <b>mavzuni</b> yozing:"
    )

@bot.message_handler(func=lambda m: m.text == "📚 Referat / Mustaqil ish")
def referat_handler(message):
    user_id = message.from_user.id
    user_data[user_id] = {"service": "Referat / Mustaqil ish"}
    set_state(user_id, STATE_WAIT_TOPIC)

    bot.send_message(
        message.chat.id,
        "📚 <b>Referat / Mustaqil ish</b>\n\n"
        "✍️ Iltimos, <b>mavzuni</b> yozing:"
    )

@bot.message_handler(func=lambda m: m.text == "🧪 Test")
def test_handler(message):
    bot.send_message(
        message.chat.id,
        "🧪 Test xizmati\n\nTez orada ishga tushadi.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🧩 Krossvord")
def crossword_handler(message):
    bot.send_message(
        message.chat.id,
        "🧩 Krossvord xizmati\n\nTez orada ishga tushadi.",
        reply_markup=main_menu()
    )

# ================== TOPIC INPUT ==================
@bot.message_handler(func=lambda m: get_state(m.from_user.id) == STATE_WAIT_TOPIC)
def topic_handler(message):
    user_id = message.from_user.id
    topic = message.text.strip()

    if len(topic) < 5:
        bot.send_message(
            message.chat.id,
            "❗ Mavzu juda qisqa.\nIltimos, aniqroq yozing:"
        )
        return

    service = user_data[user_id]["service"]

    bot.send_message(
        message.chat.id,
        "✅ <b>Mavzu qabul qilindi!</b>\n\n"
        f"🛠 Xizmat: <b>{service}</b>\n"
        f"📌 Mavzu: <b>{topic}</b>\n\n"
        "Keyingi bosqichlar (hajm, narx, demo) tez orada qo‘shiladi.",
        reply_markup=main_menu()
    )

    reset_user(user_id)

# ================== INFO ==================
@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balance_handler(message):
    bot.send_message(
        message.chat.id,
        "💰 <b>Balans:</b> 0 so‘m\n\n(To‘lov tizimi keyin ulanadi)",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "ℹ️ Qo'llanma")
def help_handler(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ <b>Qo'llanma</b>\n\n"
        "1️⃣ Xizmat tanlang\n"
        "2️⃣ Mavzu yozing\n"
        "3️⃣ Natijani oling",
        reply_markup=main_menu()
    )

Bekzod, [02.02.2026 1:13]
# ================== FALLBACK ==================
@bot.message_handler(func=lambda m: True)
def fallback_handler(message):
    bot.send_message(
        message.chat.id,
        "❗ Iltimos, menyudan foydalaning.",
        reply_markup=main_menu()
    )

# ================== RUN ==================
print("Bot PRO rejimda ishga tushdi")
bot.infinity_polling(skip_pending=True)
