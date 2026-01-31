# ===== DESIGN =====
    if state == WAIT_DESIGN:
        user_data[uid]["design"] = text
        user_data[uid]["state"] = WAIT_SIZE

        bot.send_message(
            message.chat.id,
            "📐 <b>Slaydlar sonini yozing</b>:"
        )
        return

    # ===== SIZE =====
    if state == WAIT_SIZE:
        if not text.isdigit():
            bot.send_message(message.chat.id, "❗ Faqat raqam kiriting.")
            return

        size = int(text)
        user_data[uid]["size"] = size

        base_price = size * 5000
        if user_data[uid]["premium"]:
            base_price = int(base_price * 1.5)

        user_data[uid]["state"] = WAIT_PREVIEW

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add("✏️ Tahrirlash", "✅ Tasdiqlash va PDF")

        bot.send_message(
            message.chat.id,
            f"🧾 <b>Buyurtma preview</b>\n\n"
            f"📌 Xizmat: {user_data[uid]['service']}\n"
            f"✍️ Mavzu: {user_data[uid]['topic']}\n"
            f"📐 Hajm: {size}\n"
            f"⭐ Premium: {'Yoqilgan' if user_data[uid]['premium'] else 'O‘chiq'}\n"
            f"💰 Narx: {base_price:,} so‘m\n\n"
            "📄 Avval matn beriladi, keyin PDF.",
            reply_markup=kb
        )
        return

    # ===== PREVIEW =====
    if state == WAIT_PREVIEW:
        if text == "✏️ Tahrirlash":
            user_data[uid]["state"] = WAIT_TOPIC
            bot.send_message(
                message.chat.id,
                "✍️ Qaysi joyini o‘zgartiramiz? Yozing:"
            )
            return

        if text == "✅ Tasdiqlash va PDF":
            bot.send_message(
                message.chat.id,
                "📄 PDF tayyorlanmoqda...\n"
                "⏳ Iltimos, kuting."
            )
            return

    bot.send_message(
        message.chat.id,
        "ℹ️ Iltimos, menyu orqali davom eting."
    )

# =====================
# RUN
# =====================
bot.infinity_polling(skip_pending=True)
