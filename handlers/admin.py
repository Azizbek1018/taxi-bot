# ==========================================
#   ADMIN PANEL (faqat haydovchi uchun)
# ==========================================

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database import get_driver_data, update_driver_data
from keyboards import admin_panel_kb
from states import AdminStates

router = Router()

# Ushbu routerdagi BARCHA handlerlar faqat ADMIN_ID uchun ishlaydi.
# Boshqa foydalanuvchilarning xabarlari avtomatik ravishda keyingi routerga o'tadi.
router.message.filter(F.from_user.id == ADMIN_ID)
router.callback_query.filter(F.from_user.id == ADMIN_ID)


def _current_info_text() -> str:
    d = get_driver_data()
    return (
        "🔐 <b>Admin panel</b>\n\n"
        f"👤 Ism: {d['driver_name']}\n"
        f"🚘 Mashina: {d['car_model']}\n"
        f"🔢 Davlat raqami: {d['car_number']}\n"
        f"📞 Telefon: {d['phone']}\n"
        f"📊 Holat: {d['status']}\n\n"
        "Quyidagi bo'limlardan birini tanlang 👇"
    )


@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(_current_info_text(), reply_markup=admin_panel_kb())


@router.callback_query(F.data == "admin_view")
async def admin_view(callback: CallbackQuery):
    d = get_driver_data()
    text = (
        f"👤 Ism: {d['driver_name']}\n"
        f"🚘 Mashina: {d['car_model']}\n"
        f"🔢 Davlat raqami: {d['car_number']}\n"
        f"📞 Telefon: {d['phone']}\n"
        f"📊 Holat: {d['status']}"
    )
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "admin_car")
async def admin_car(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_car_model)
    await callback.message.answer(
        "Yangi mashina rusumi va davlat raqamini quyidagi formatda yuboring "
        "(ikkalasini <b>/</b> belgisi bilan ajrating):\n\n"
        "<code>Chevrolet Cobalt / 01 A 123 AA</code>"
    )
    await callback.answer()


@router.message(AdminStates.waiting_car_model)
async def set_car(message: Message, state: FSMContext):
    if "/" not in (message.text or ""):
        await message.answer(
            "⚠️ Format noto'g'ri. Iltimos, quyidagicha yuboring:\n\n"
            "<code>Mashina rusumi / Davlat raqami</code>"
        )
        return

    model, number = [part.strip() for part in message.text.split("/", 1)]
    update_driver_data("car_model", model)
    update_driver_data("car_number", number)

    await state.clear()
    await message.answer("✅ Mashina ma'lumotlari muvaffaqiyatli yangilandi.")


@router.callback_query(F.data == "admin_phone")
async def admin_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_phone)
    await callback.message.answer(
        "Yangi telefon raqamni yuboring (masalan: +998901234567):"
    )
    await callback.answer()


@router.message(AdminStates.waiting_phone)
async def set_phone(message: Message, state: FSMContext):
    update_driver_data("phone", message.text.strip())
    await state.clear()
    await message.answer("✅ Telefon raqam muvaffaqiyatli yangilandi.")


@router.callback_query(F.data == "admin_status")
async def admin_status(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_status)
    await callback.message.answer(
        "Yangi holat/e'lon matnini yuboring.\n\nMasalan:\n"
        "✅ Bo'sh joylar bor\n"
        "❌ Joylar qolmadi"
    )
    await callback.answer()


@router.message(AdminStates.waiting_status)
async def set_status(message: Message, state: FSMContext):
    update_driver_data("status", message.text.strip())
    await state.clear()
    await message.answer("✅ Holat/e'lon matni muvaffaqiyatli yangilandi.")
