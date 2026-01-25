# === pdf_generator.py (PRO 1.1 — tuzatilgan) ===
from fpdf import FPDF
import os

def create_pdf(title, content, filename):
    """Matndan PDF hujjat yaratish (O‘zbekcha matn uchun to‘liq ishlaydi)"""
    try:
        pdf = FPDF()
        pdf.add_page()

        # Kirillcha shriftni qo‘shamiz
        font_path = os.path.join(os.path.dirname(file), "DejaVuSans.ttf")
        if os.path.exists(font_path):
            pdf.add_font("DejaVu", "", font_path, uni=True)
            pdf.set_font("DejaVu", size=12)
        else:
            pdf.set_font("Arial", size=12)

        # Sarlavha
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"{title}", ln=True, align="C")
        pdf.ln(10)

        # Matn
        pdf.set_font("Arial", size=12)
        lines = content.split("\n")
        for line in lines:
            pdf.multi_cell(0, 8, line)

        # PDF ni saqlash
        pdf.output(filename)
        print(f"[INFO] PDF tayyorlandi: {filename}")
        return filename

    except Exception as e:
        print(f"[ERROR] PDF yaratishda xato: {e}")
        return None
