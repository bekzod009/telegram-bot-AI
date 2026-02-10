import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from openai import OpenAI

# === ENV ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("ENV o‘zgaruvchilar yetishmayapti")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
client = OpenAI(api_key=OPENAI_API_KEY)

# === USER STATES ===
user_state = {}

# === MENYU ===
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📄 Referat"),
        KeyboardButton("📝 Mustaqil ish"),
    )
    kb.add(
        KeyboardButton("📘 Kurs ishi"),
        KeyboardButton("📊 Slayd"),
    )
    return kb

# === START ===
@bot.message_handler(commands=["start"])
def start(msg):
    user_state[msg.chat.id] = {}
    bot.send_message(
        msg.chat.id,
        "👋 <b>Xush kelibsiz!</b>\n\n"
        "Quyidagi xizmatlardan birini tanlang:",
        reply_markup=main_menu()
    )

# === XIZMAT TANLASH ===
@bot.message_handler(func=lambda m: m.text in [
    "📄 Referat",
    "📝 Mustaqil ish",
    "📘 Kurs ishi",
    "📊 Slayd"
])
def choose_service(msg):
    user_state[msg.chat.id] = {
        "service": msg.text,
        "step": "waiting_topic"
    }
    bot.send_message(
        msg.chat.id,
        f"✅ <b>{msg.text}</b> tanlandi.\n\n"
        "✍️ Endi mavzuni yozing:"
    )

# === MAVZU QABUL QILISH ===
@bot.message_handler(func=lambda m: user_state.get(m.chat.id, {}).get("step") == "waiting_topic")
def handle_topic(msg):
    service = user_state[msg.chat.id]["service"]
    topic = msg.text

    bot.send_message(msg.chat.id, "⏳ AI ishlayapti, iltimos kuting...")

    prompt = f"""
Siz professional ta'lim kontent yaratuvchisiz.

Xizmat turi: {service}
Mavzu: {topic}

Iltimos:
- rasmiy
- tushunarli
- mantiqiy tuzilgan
matn tayyorlang.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Siz ta'lim uchun kontent tayyorlaysiz."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900
        )

        result = response.choices[0].message.content
        bot.send_message(msg.chat.id, result)

        # holatni tozalaymiz
        user_state[msg.chat.id] = {}

    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Xatolik: {e}")

# === DEFAULT ===
@bot.message_handler(func=lambda m: True)
def fallback(msg):
    bot.send_message(
        msg.chat.id,
        "❗ Iltimos, menyudan xizmat tanlang yoki /start ni bosing."
    )

# === RUN ===
bot.infinity_polling(skip_pending=True)
