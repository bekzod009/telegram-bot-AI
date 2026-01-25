# === config.py (FINAL PRO EDITION) ===

# Telegram bot tokeningiz
TOKEN = "8321742240:AAHFwAQEYpZNReK_GrGIY_wx4K4bz5XqWOE"

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
