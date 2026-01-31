Bekzod, [01.02.2026 1:32]
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== TOKEN ==================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi (Environment Variables ni tekshir)")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================== USER STATE ==================
user_state = {}
user_data = {}

WAIT_SLIDE_TOPIC = "wait_slide_topic"
WAIT_DEMO_CONFIRM = "wait_demo_confirm"

# ================== KEYBOARDS ==================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📊 Slayd yaratish"),
        KeyboardButton("📚 Referat / Mustaqil ish")
    )
    kb.add(
        KeyboardButton("ℹ️ Qo'llanma"),
        KeyboardButton("⚙️ Sozlamalar")
    )
    return kb


def confirm_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("✅ Tasdiqlash"),
        KeyboardButton("✏️ Tahrirlash"),
        KeyboardButton("❌ Bekor qilish")
    )
    return kb

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    user_state[user_id] = None
    user_data[user_id] = {}

    bot.send_message(
        user_id,
        "👋 <b>Assalomu alaykum!</b>\n\n"
        "Bu bot orqali slayd, referat va boshqa ishlarni tayyorlashingiz mumkin.\n\n"
        "Boshlash uchun xizmat tanlang 👇",
        reply_markup=main_menu()
    )

# ================== SLAYD ==================
@bot.message_handler(func=lambda m: m.text == "📊 Slayd yaratish")
def slide_start(message):
    user_id = message.chat.id
    user_state[user_id] = WAIT_SLIDE_TOPIC

    bot.send_message(
        user_id,
        "📊 <b>Slayd xizmati</b>\n\n"
        "Iltimos, <b>mavzuni to‘liq va aniq</b> yozing:",
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )

# ================== SLAYD TOPIC ==================
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == WAIT_SLIDE_TOPIC)
def slide_topic(message):
    user_id = message.chat.id
    topic = message.text.strip()

    if len(topic) < 5:
        bot.send_message(user_id, "❗️ Mavzu juda qisqa. Iltimos, aniqroq yozing.")
        return

    user_data[user_id]["topic"] = topic
    user_state[user_id] = WAIT_DEMO_CONFIRM

    # ===== DEMO MATN (BEPUL) =====
    demo_text = (
        f"✅ <b>DEMO SLAYD MATNI</b>\n\n"
        f"📌 <b>Mavzu:</b> {topic}\n\n"
        "1️⃣ Kirish\n"
        f"{topic} mavzusining dolzarbligi va ahamiyati.\n\n"
        "2️⃣ Asosiy qism\n"
        "Mavzu bo‘yicha asosiy tushunchalar va tahlil.\n\n"
        "3️⃣ Xulosa\n"
        "Asosiy natijalar va umumiy xulosalar.\n\n"
        "ℹ️ Bu faqat <b>DEMO</b>. Tasdiqlangandan so‘ng to‘liq slayd tayyorlanadi."
    )

    bot.send_message(
        user_id,
        demo_text,
        reply_markup=confirm_menu()
    )

# ================== DEMO CONFIRM ==================
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == WAIT_DEMO_CONFIRM)
def slide_confirm(message):
    user_id = message.chat.id
    text = message.text

    if text == "✅ Tasdiqlash":
        bot.send_message(
            user_id,
            "💳 Keyingi bosqichda to‘lov va slayd dizayni tanlanadi.\n\n"
            "⏳ Tez orada ishga tushadi.",
            reply_markup=main_menu()
        )
        user_state[user_id] = None

    elif text == "✏️ Tahrirlash":
        user_state[user_id] = WAIT_SLIDE_TOPIC
        bot.send_message(
            user_id,
            "✏️ Yangi mavzuni kiriting:",
            reply_markup=telebot.types.ReplyKeyboardRemove()
        )

    elif text == "❌ Bekor qilish":
        user_state[user_id] = None
        bot.send_message(
            user_id,
            "❌ Buyurtma bekor qilindi.",
            reply_markup=main_menu()
        )

    else:
        bot.send_message(user_id, "Iltimos, tugmalardan foydalaning.")

Bekzod, [01.02.2026 1:32]
# ================== OTHER ==================
@bot.message_handler(func=lambda m: True)
def other(message):
    bot.send_message(
        message.chat.id,
        "❗️ Iltimos, menyudan foydalaning.",
        reply_markup=main_menu()
    )

# ================== RUN ==================
print("Bot started (SLAYD DEMO)")
bot.infinity_polling()
