
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from openai import OpenAI

# ================= TOKEN =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi (Render env)")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY topilmadi (Render env)")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
client = OpenAI(api_key=OPENAI_API_KEY)

# ================= STATE =================
STATE_NONE = "NONE"
STATE_REFERAT = "REFERAT"
STATE_SLAYD = "SLAYD"
STATE_KURS = "KURS"

user_state = {}

def set_state(uid, state):
    user_state[uid] = state

def get_state(uid):
    return user_state.get(uid, STATE_NONE)

# ================= MENU =================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📄 Referat"),
        KeyboardButton("📊 Slayd"),
        KeyboardButton("🎓 Kurs ishi")
    )
    kb.add(KeyboardButton("ℹ️ Qo'llanma"))
    return kb

# ================= AI =================
def ai_generate(prompt: str) -> str:
    try:
        r = client.responses.create(
            model="gpt-5.2",
            input=prompt
        )
        return r.output_text.strip()
    except Exception as e:
        return f"❌ AI xatosi: {e}"

# ================= START =================
@bot.message_handler(commands=["start"])
def start(message):
    set_state(message.from_user.id, STATE_NONE)
    bot.send_message(
        message.chat.id,
        "👋 <b>Salom!</b>\n\n"
        "AI yordamida:\n"
        "📄 Referat\n"
        "📊 Slayd\n"
        "🎓 Kurs ishi\n\n"
        "yaratishingiz mumkin.",
        reply_markup=main_menu()
    )

# ================= REFERAT =================
@bot.message_handler(func=lambda m: m.text == "📄 Referat")
def referat_start(message):
    set_state(message.from_user.id, STATE_REFERAT)
    bot.send_message(message.chat.id, "✍️ Referat mavzusini yozing:")

# ================= SLAYD =================
@bot.message_handler(func=lambda m: m.text == "📊 Slayd")
def slayd_start(message):
    set_state(message.from_user.id, STATE_SLAYD)
    bot.send_message(
        message.chat.id,
        "📊 Slayd mavzusini yozing:\n\n"
        "Masalan: <i>O'zbekiston iqtisodiyoti</i>"
    )

# ================= KURS ISHI =================
@bot.message_handler(func=lambda m: m.text == "🎓 Kurs ishi")
def kurs_start(message):
    set_state(message.from_user.id, STATE_KURS)
    bot.send_message(
        message.chat.id,
        "🎓 Kurs ishi mavzusini yozing:"
    )

# ================= TEXT HANDLER =================
@bot.message_handler(func=lambda m: get_state(m.from_user.id) != STATE_NONE)
def handle_text(message):
    uid = message.from_user.id
    text = message.text.strip()

    bot.send_message(message.chat.id, "⏳ AI ishlayapti, kuting...")

    if get_state(uid) == STATE_REFERAT:
        prompt = f"""
Akademik uslubda referat yoz.
Til: O'zbek
Hajm: o'rtacha

Mavzu:
{text}
"""

    elif get_state(uid) == STATE_SLAYD:
        prompt = f"""
PowerPoint slayd uchun MATN tayyorla.
10 slayd bo'lsin.
Har bir slayd uchun sarlavha va qisqa punktlar yoz.

Mavzu:
{text}
"""

    elif get_state(uid) == STATE_KURS:
        prompt = f"""
Kurs ishi yoz.
Struktura:
- Kirish
- Asosiy qism (2 bo'lim)
- Xulosa
- Foydalanilgan adabiyotlar

Til: O'zbek
Akademik uslub.

Mavzu:
{text}
"""

    else:
        return

    result = ai_generate(prompt)
    bot.send_message(message.chat.id, result)
    set_state(uid, STATE_NONE)

# ================= HELP =================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Qo'llanma")
def help_menu(message):
    bot.send_message(
        message.chat.id,
        "📘 <b>Qo'llanma</b>\n\n"
        "1️⃣ Xizmat tanlang\n"
        "2️⃣ Mavzu yozing\n"
        "3️⃣ AI natijani beradi\n\n"
        "📌 Slayd – matn shaklida\n"
        "📌 Kurs ishi – to‘liq struktura",
        reply_markup=main_menu()
    )

# ================= FALLBACK =================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "❗ Menyudan foydalaning.",
        reply_markup=main_menu()
    )

# ================= RUN =================
print("🚀 Bot PRO + AI ishlayapti")
bot.infinity_polling(skip_pending=True)
