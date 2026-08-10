# ==========================================
#   BOT SOZLAMALARI (CONFIG)
# ==========================================
# Maxfiy ma'lumotlar (TOKEN, ADMIN_ID) ".env" faylidan o'qiladi.
# ".env" fayl hech qachon GitHub'ga yuklanmaydi (.gitignore ichida).
#
# Sozlash uchun:
#   1) ".env.example" faylidan nusxa oling: cp .env.example .env
#   2) ".env" faylini oching va o'z TOKEN/ID qiymatlaringizni kiriting.

import os
import sys

from dotenv import load_dotenv

load_dotenv()  # ".env" faylidagi o'zgaruvchilarni yuklaydi

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_RAW = os.getenv("ADMIN_ID")

# Bot ishga tushishidan oldin sozlamalar to'g'ri kiritilganini tekshiramiz.
if not BOT_TOKEN:
    sys.exit(
        "❌ XATOLIK: BOT_TOKEN topilmadi.\n"
        "Iltimos, '.env' faylini yarating (namuna: .env.example) va "
        "BOT_TOKEN qiymatini kiriting."
    )

if not ADMIN_ID_RAW or not ADMIN_ID_RAW.strip().lstrip("-").isdigit():
    sys.exit(
        "❌ XATOLIK: ADMIN_ID noto'g'ri yoki topilmadi.\n"
        "Iltimos, '.env' faylida ADMIN_ID ni faqat raqamlar bilan kiriting "
        "(masalan: ADMIN_ID=123456789)."
    )

ADMIN_ID = int(ADMIN_ID_RAW.strip())
