# ==========================================
#   GURUHLARGA AVTOMATIK REKLAMA
# ==========================================

from aiogram import Router, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER
from aiogram.types import ChatMemberUpdated, Message

from config import ADMIN_ID
from database import get_driver_data

router = Router()


def ad_text() -> str:
    """Guruhga tashlanadigan chiroyli, ishonch uyg'otuvchi reklama matni."""
    d = get_driver_data()
    return (
        "🚕 <b>Ishonchli taksi xizmati — Samarqand ⇄ Toshkent</b> 🚕\n\n"
        f"Assalomu alaykum, hurmatli a'zolar! Men — <b>{d['driver_name']}</b>, "
        "Samarqand va Toshkent oralig'ida har kuni qatnovchi shaxsiy haydovchiman.\n\n"
        f"🚘 Mashina: <b>{d['car_model']}</b>\n"
        f"🔢 Davlat raqami: <b>{d['car_number']}</b>\n"
        f"📞 Bog'lanish: <b>{d['phone']}</b>\n"
        f"📊 Holat: <b>{d['status']}</b>\n\n"
        "🛡 Xavfsizlik, tozalik va vaqtida yetib borish — bizning asosiy tamoyillarimiz. "
        "Mashinaga <b>maksimal 4 nafar</b> yo'lovchi olinadi, shu bois har bir yo'lovchiga "
        "qulay va xavfsiz sayohat kafolatlanadi.\n\n"
        "✅ Buyurtma berish uchun botga shaxsiy xabar yozing va \"Buyurtma berish\" "
        "tugmasini bosing.\n\n"
        "Ishonchingiz biz uchun qadrli! 💛"
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def on_bot_added_to_group(event: ChatMemberUpdated):
    """Bot biror guruhga qo'shilganda avtomatik reklama yuboradi."""
    await event.bot.send_message(event.chat.id, ad_text())


@router.message(Command("reklama"), F.chat.type.in_({"group", "supergroup"}))
async def post_ad_manually(message: Message):
    """Guruh ichida /reklama buyrug'i orqali qo'lda reklama joylash (faqat haydovchi uchun)."""
    if message.from_user.id != ADMIN_ID:
        await message.answer("⚠️ Bu buyruqni faqat haydovchi ishlata oladi.")
        return
    await message.answer(ad_text())
