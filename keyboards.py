# ==========================================
#   KLAVIATURALAR (TUGMALAR)
# ==========================================

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    """Mijoz uchun asosiy menyu."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="🚕 Buyurtma berish")
    builder.button(text="ℹ️ Ma'lumot")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def direction_kb() -> InlineKeyboardMarkup:
    """Yo'nalishni tanlash uchun inline tugmalar."""
    builder = InlineKeyboardBuilder()
    builder.button(text="Samarqand ➔ Toshkent", callback_data="dir_samarqand_toshkent")
    builder.button(text="Toshkent ➔ Samarqand", callback_data="dir_toshkent_samarqand")
    builder.adjust(1)
    return builder.as_markup()


def contact_kb() -> ReplyKeyboardMarkup:
    """Kontakt ulashish tugmasi."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="📞 Raqamni ulashish", request_contact=True)
    builder.button(text="⬅️ Bekor qilish")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def cancel_kb() -> ReplyKeyboardMarkup:
    """Jarayonni bekor qilish tugmasi."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="⬅️ Bekor qilish")
    return builder.as_markup(resize_keyboard=True)


def admin_panel_kb() -> InlineKeyboardMarkup:
    """Admin panel bosh menyusi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🚘 Mashina ma'lumoti", callback_data="admin_car")
    builder.button(text="📞 Telefon raqam", callback_data="admin_phone")
    builder.button(text="📝 Holat / e'lon matni", callback_data="admin_status")
    builder.button(text="👀 Joriy ma'lumotlarni ko'rish", callback_data="admin_view")
    builder.adjust(1)
    return builder.as_markup()
