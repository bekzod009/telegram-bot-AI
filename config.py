# === bot.py (PRO versiya) ===
import telebot
from telebot import types
from config import TOKEN, PRICING, ADMIN_ID
from payments import send_payment_info, auto_confirm_payment
from user_data import get_balance, update_balance, add_order, get_user_orders
from pdf_generator import create_pdf

bot = telebot.TeleBot(TOKEN)

# Har bir foydalanuvchi uchun vaqtinchalik ma'lumotlar
user_state = {}

# --- /start komandasi ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🧾 Buyurtma berish", "💰 Balans", "📜 Tarix")
    bot.send_message(
        message.chat.id,
        f"👋 Assalomu alaykum, {message.from_user.first_name}!\n"
        "Men siz uchun referat, taqdimot va kurs ishlarini PDF shaklida tayyorlayman.\n\n"
        "Quyidagi menyudan keraklisini tanlang:",
        reply_markup=markup
    )

# --- Balans menyusi ---
@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balance_check(message):
    bal = get_balance(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"💰 Sizning joriy balansingiz: {bal} so‘m.\n\n"
        "Balansni to‘ldirish uchun /buy komandasini yozing."
    )

# --- To‘lov uchun ---
@bot.message_handler(commands=['buy'])
def buy(message):
    send_payment_info(bot, message)

# --- Chek yuborilganda ---
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    auto_confirm_payment(bot, message)

# --- Buyurtma menyusi ---
@bot.message_handler(func=lambda m: m.text == "🧾 Buyurtma berish")
def order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Referat", "💼 Kurs ishi", "🎞️ Taqdimot")
    bot.send_message(
        message.chat.id,
        "Qaysi turdagi ishni xohlaysiz?",
        reply_markup=markup
    )

# --- Referat tanlansa ---
@bot.message_handler(func=lambda m: m.text == "📚 Referat")
def referat(message):
    msg = bot.send_message(message.chat.id, "📘 Iltimos, referat mavzusini kiriting:")
    bot.register_next_step_handler(msg, get_topic)

def get_topic(message):
    user_state[message.chat.id] = {"topic": message.text}
    msg = bot.send_message(message.chat.id, "Endi referat matnini yozing yoki yuboring:")
    bot.register_next_step_handler(msg, generate_pdf)

# --- PDF yaratish ---
def generate_pdf(message):
    topic = user_state[message.chat.id]["topic"]
    content = message.text

    filename = f"{topic}.pdf"
    create_pdf(topic, content, filename)

    with open(filename, "rb") as f:
        bot.send_document(message.chat.id, f)

    # Buyurtma tarixiga yozish
    order_info = {
        "tur": "Referat",
        "fan": topic,
        "narx": 5000,
        "status": "Tayyor"
    }
    add_order(message.chat.id, order_info)

    bot.send_message(message.chat.id, "✅ Referat PDF shaklida tayyorlandi!")
    del user_state[message.chat.id]

# --- Kurs ishi ---
@bot.message_handler(func=lambda m: m.text == "💼 Kurs ishi")
def kurs_ishi(message):
    msg = bot.send_message(message.chat.id, "📗 Kurs ishi mavzusini kiriting:")
    bot.register_next_step_handler(msg, process_kurs_ishi)

def process_kurs_ishi(message):
    topic = message.text
    bot.send_message(message.chat.id, f"✅ Kurs ishi uchun ma’lumot qabul qilindi: *{topic}*", parse_mode="Markdown")

    order_info = {
        "tur": "Kurs ishi",
        "fan": topic,
        "narx": 30000,
        "status": "Jarayonda"
    }
    add_order(message.chat.id, order_info)
    bot.send_message(message.chat.id, "💰 To‘lovni amalga oshiring va chekni yuboring.")
    send_payment_info(bot, message)

# --- Taqdimot (slayd) ---
@bot.message_handler(func=lambda m: m.text == "🎞️ Taqdimot")
def taqdimot(message):
    msg = bot.send_message(message.chat.id, "🎯 Taqdimot mavzusini kiriting:")
    bot.register_next_step_handler(msg, get_presentation_topic)

Bekzod, [20.01.2026 1:04]
def get_presentation_topic(message):
    topic = message.text
    bot.send_message(message.chat.id, f"✅ Mavzu qabul qilindi: {topic}\n"
                                      "Endi slaydlar sonini kiriting (1 dan 60 gacha):")
    bot.register_next_step_handler(message, process_slides, topic)

def process_slides(message, topic):
    try:
        slides = int(message.text)
        if slides < 1 or slides > 60:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Iltimos, 1 dan 60 gacha raqam kiriting.")
        return

    bot.send_message(message.chat.id, f"📊 {slides} betlik taqdimot tayyorlanmoqda...")

    order_info = {
        "tur": "Taqdimot",
        "fan": topic,
        "narx": 10000 if slides <= 30 else 15000,
        "status": "Jarayonda"
    }
    add_order(message.chat.id, order_info)

    bot.send_message(message.chat.id, "💰 To‘lovni amalga oshiring va chekni yuboring.")
    send_payment_info(bot, message)

# --- Tarix ---
@bot.message_handler(func=lambda m: m.text == "📜 Tarix")
def history(message):
    orders = get_user_orders(message.chat.id)
    if not orders:
        bot.send_message(message.chat.id, "Sizda hali buyurtma tarixi yo‘q.")
        return

    text = "📜 Buyurtma tarixi:\n\n"
    for i, order in enumerate(orders, 1):
        text += f"{i}. {order['tur']} – {order['fan']}\n"
        text += f"   💰 {order['narx']} so‘m | {order['status']}\n\n"

    bot.send_message(message.chat.id, text)

# --- Admin kuzatuv ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
        return

    all_orders = get_user_orders(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"🧮 Buyurtmalar soni: {len(all_orders)} ta\n"
        f"📈 So‘nggi foydalanuvchi: {message.from_user.username or message.chat.id}"
    )

bot.polling(none_stop=True)

Bekzod, [20.01.2026 1:14]
# === config.py (FINAL PRO EDITION) ===

# Telegram bot tokeningiz
# Admin ID — bu sizning Telegram ID raqamingiz
ADMIN_ID = 123456789  # <-- bu yerga o‘zingizning Telegram ID raqamingizni yozing

# Narxlar (so‘mda)
PRICING = {
    "referat": 5000,
    "kurs_ishi": 30000,
    "taqdimot_30": 10000,
    "taqdimot_60": 15000
}

# To‘lov tizimi ma’lumotlari (ikkita karta bilan)
PAYMENT_CONFIG = {
    "cards": [
        {
            "card_number": "9860 0901 0898 1672",
            "card_name": "BEKZOD HAYDAROV",
            "type": "UZCARD"
        },
        {
            "card_number": "8600 1404 6499 6132",
            "card_name": "BEKZOD HAYDAROV",
            "type": "HUMO"
        }
    ],
    "instructions": (
        "💳 To‘lovni amalga oshirish uchun quyidagi kartalardan biriga o‘tkazing:\n\n"
        "💰 *9860 0901 0898 1672* — BEKZOD HAYDAROV (UZCARD)\n"
        "💰 *8600 1404 6499 6132* — BEKZOD HAYDAROV (HUMO)\n\n"
        "✅ To‘lovni amalga oshirgach, chek rasmini botga yuboring.\n"
        "♻️ To‘lov tasdiqlangach, balansingiz avtomatik to‘ldiriladi."
    )
}

# Qo‘shimcha sozlamalar
BOT_SETTINGS = {
    "language": "uz",
    "version": "PRO 1.0",
    "developer": "Bekzod Dev Team",
    "support_contact": "@bekzod_support",
    "copyright": "© 2026 Bekzod Dev Team. All rights reserved."
}
