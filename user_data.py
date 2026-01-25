# === user_data.py (PRO 1.1) ===
import json
import os

DATA_FILE = "user_data.json"

# --- Ma'lumotlarni yuklash ---
def load_data():
    """Foydalanuvchi ma'lumotlarini yuklaydi"""
    if not os.path.exists(DATA_FILE):
        save_data({})
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        save_data({})
        return {}

# --- Ma'lumotlarni saqlash ---
def save_data(data):
    """Ma'lumotlarni JSON faylga saqlaydi"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Ma'lumotni saqlashda xato: {e}")

# --- Foydalanuvchi mavjudligini tekshirish ---
def ensure_user_exists(user_id):
    """Agar foydalanuvchi mavjud bo‘lmasa, uni yaratadi"""
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"balance": 0, "orders": []}
        save_data(data)
    return data

# --- Balansni olish ---
def get_balance(user_id):
    data = ensure_user_exists(user_id)
    return data[str(user_id)]["balance"]

# --- Balansni yangilash ---
def update_balance(user_id, amount):
    data = ensure_user_exists(user_id)
    uid = str(user_id)
    data[uid]["balance"] += int(amount)
    save_data(data)

# --- Buyurtma qo‘shish ---
def add_order(user_id, order_info):
    data = ensure_user_exists(user_id)
    uid = str(user_id)
    data[uid]["orders"].append(order_info)
    save_data(data)

# --- Buyurtmalar tarixini olish ---
def get_user_orders(user_id):
    data = ensure_user_exists(user_id)
    return data[str(user_id)].get("orders", [])

# --- Balansni kamaytirish (masalan, to‘lovdan so‘ng) ---
def reduce_balance(user_id, amount):
    data = ensure_user_exists(user_id)
    uid = str(user_id)
    if data[uid]["balance"] >= amount:
        data[uid]["balance"] -= amount
        save_data(data)
        return True
    return False
