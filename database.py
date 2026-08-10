# ==========================================
#   HAYDOVCHI MA'LUMOTLARI BILAN ISHLASH
# ==========================================
# Ma'lumotlar oddiy JSON faylda saqlanadi, shuning uchun
# bot qayta ishga tushirilganda ham ma'lumotlar yo'qolmaydi.

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "driver_data.json")

# Bot birinchi marta ishga tushganda ishlatiladigan standart ma'lumotlar.
# Bu qiymatlarni keyinchalik /admin panel orqali o'zgartirish mumkin.
DEFAULT_DATA = {
    "driver_name": "Alisher Nazarov",
    "car_model": "Chevrolet Malibu 2",
    "car_number": "01 A 777 AA",
    "phone": "+998 90 123 45 67",
    "status": "✅ Bo'sh joylar bor",
}


def _ensure_file() -> None:
    """Ma'lumotlar fayli mavjud bo'lmasa, standart qiymatlar bilan yaratadi."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=4)


def get_driver_data() -> dict:
    """Joriy haydovchi ma'lumotlarini qaytaradi."""
    _ensure_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def update_driver_data(key: str, value: str) -> None:
    """Berilgan kalit bo'yicha ma'lumotni yangilaydi va faylga saqlaydi."""
    data = get_driver_data()
    data[key] = value
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
