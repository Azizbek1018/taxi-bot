# ==========================================
#   MIJOZLAR UCHUN HANDLERLAR
#   (/start, ma'lumot, buyurtma berish jarayoni)
# ==========================================

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database import get_driver_data
from keyboards import main_menu_kb, direction_kb, contact_kb, cancel_kb
from states import OrderStates

router = Router()

# callback_data -> o'qiladigan yo'nalish nomi
DIRECTIONS = {
    "dir_samarqand_toshkent": "Samarqand ➔ Toshkent",
    "dir_toshkent_samarqand": "Toshkent ➔ Samarqand",
}


def driver_info_text() -> str:
    """Haydovchi haqida ishonch uyg'otuvchi, samimiy matn shakllantiradi."""
    d = get_driver_data()
    return (
        "👋 Assalomu alaykum, hurmatli mijoz!\n\n"
        f"Men — <b>{d['driver_name']}</b>, Samarqand ⇄ Toshkent yo'nalishida ishonchli "
        "va vaqtida yetkazib beruvchi shaxsiy taksi xizmatini taqdim etaman. 🚕\n\n"
        f"🚘 <b>Mashina:</b> {d['car_model']}\n"
        f"🔢 <b>Davlat raqami:</b> {d['car_number']}\n"
        f"📞 <b>Telefon:</b> {d['phone']}\n"
        f"📊 <b>Holat:</b> {d['status']}\n\n"
        "🛡 <i>Xavfsizlik va qulaylik biz uchun ustuvor — shu bois mashinaga maksimal "
        "4 nafar yo'lovchi olinadi.</i>\n\n"
        "Ishonch va samimiylik — bizning asosiy tamoyilimiz. Har bir mijoz o'zini xavfsiz "
        "va qadrlangan his qilishi kerak. Buyurtma berish uchun quyidagi tugmadan "
        "foydalaning 👇"
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(driver_info_text(), reply_markup=main_menu_kb())


@router.message(F.text == "ℹ️ Ma'lumot")
async def show_info(message: Message):
    await message.answer(driver_info_text())


@router.message(F.text == "⬅️ Bekor qilish")
async def cancel_any(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi. Bosh menyudasiz 👇", reply_markup=main_menu_kb())


@router.message(F.text == "🚕 Buyurtma berish")
async def start_order(message: Message, state: FSMContext):
    await state.set_state(OrderStates.choosing_direction)
    await message.answer(
        "Ajoyib! Buyurtmangizni birga rasmiylashtiramiz. 🙌",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer("Qaysi yo'nalish bo'yicha boryapsiz?", reply_markup=direction_kb())


@router.callback_query(OrderStates.choosing_direction, F.data.startswith("dir_"))
async def choose_direction(callback: CallbackQuery, state: FSMContext):
    direction = DIRECTIONS.get(callback.data)
    await state.update_data(direction=direction)
    await state.set_state(OrderStates.entering_passengers)

    await callback.message.edit_text(f"Yo'nalish tanlandi: <b>{direction}</b> ✅")
    await callback.message.answer(
        "Nechta yo'lovchi bo'lasiz?\n\n"
        "⚠️ Xavfsizlik nuqtai nazaridan mashinada <b>maksimal 4 kishi</b>ga joy bor.\n"
        "Iltimos, sonini raqam bilan yozing (masalan: 2).",
        reply_markup=cancel_kb(),
    )
    await callback.answer()


@router.message(OrderStates.entering_passengers)
async def enter_passengers(message: Message, state: FSMContext):
    text = (message.text or "").strip()

    if not text.isdigit():
        await message.answer(
            "⚠️ Iltimos, yo'lovchilar sonini faqat raqam bilan kiriting (masalan: 3)."
        )
        return

    count = int(text)

    if count <= 0:
        await message.answer("⚠️ Yo'lovchilar soni kamida 1 ta bo'lishi kerak.")
        return

    if count > 4:
        await message.answer(
            "⚠️ Afsuski, xavfsizlik va qulaylik talablariga ko'ra mashinada "
            "<b>maksimal 4 nafar yo'lovchi</b>ga joy bor.\n"
            "Iltimos, 1 dan 4 gachа bo'lgan sonni kiriting."
        )
        return

    await state.update_data(passengers=count)
    await state.set_state(OrderStates.sharing_contact)
    await message.answer(
        "Ajoyib! Endi siz bilan tezroq bog'lanishimiz uchun telefon raqamingizni yuboring.\n\n"
        "Pastdagi tugma orqali ulashishingiz mumkin, yoki qo'lda yozib yuborsangiz ham bo'ladi 📞",
        reply_markup=contact_kb(),
    )


@router.message(OrderStates.sharing_contact, F.contact)
async def get_contact(message: Message, state: FSMContext, bot: Bot):
    phone = message.contact.phone_number
    await finish_order(message, state, bot, phone)


@router.message(OrderStates.sharing_contact, F.text)
async def get_contact_text(message: Message, state: FSMContext, bot: Bot):
    phone = message.text.strip()
    digits = sum(ch.isdigit() for ch in phone)

    if digits < 7:
        await message.answer(
            "⚠️ Iltimos, to'g'ri telefon raqam kiriting yoki tugma orqali ulashing."
        )
        return

    await finish_order(message, state, bot, phone)


async def finish_order(message: Message, state: FSMContext, bot: Bot, phone: str) -> None:
    """Yig'ilgan buyurtma ma'lumotlarini adminga yuboradi va mijozga tasdiq beradi."""
    data = await state.get_data()
    direction = data.get("direction", "Noma'lum")
    passengers = data.get("passengers", "Noma'lum")

    user = message.from_user
    username_part = f"@{user.username}" if user.username else "yo'q"

    admin_text = (
        "🆕 <b>Yangi buyurtma tushdi!</b>\n\n"
        f"👤 Mijoz: {user.full_name}\n"
        f"🔗 Username: {username_part}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🧭 Yo'nalish: <b>{direction}</b>\n"
        f"👥 Yo'lovchilar soni: <b>{passengers}</b>\n"
        f"📞 Telefon: <b>{phone}</b>"
    )

    try:
        await bot.send_message(ADMIN_ID, admin_text)
    except Exception:
        # Admin botni bloklagan yoki hali /start bosmagan bo'lishi mumkin.
        pass

    await message.answer(
        "✅ Buyurtmangiz muvaffaqiyatli qabul qilindi!\n\n"
        "Tez orada haydovchi shaxsan siz bilan bog'lanadi. Bizga ishonganingiz uchun rahmat — "
        "yo'lingiz xavfsiz va qulay bo'lishi uchun barcha choralarni ko'ramiz. 🚕💛",
        reply_markup=main_menu_kb(),
    )
    await state.clear()
