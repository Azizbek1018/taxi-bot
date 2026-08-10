# ==========================================
#   FSM HOLATLARI (STATES)
# ==========================================

from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """Mijoz buyurtma berish jarayonidagi bosqichlar."""
    choosing_direction = State()      # Yo'nalishni tanlash
    entering_passengers = State()     # Yo'lovchilar sonini kiritish
    sharing_contact = State()         # Telefon raqamni yuborish


class AdminStates(StatesGroup):
    """Admin panel orqali ma'lumotlarni tahrirlash bosqichlari."""
    waiting_car_model = State()       # Mashina rusumi + raqamini kutish
    waiting_phone = State()           # Yangi telefon raqamni kutish
    waiting_status = State()          # Yangi holat/e'lon matnini kutish
