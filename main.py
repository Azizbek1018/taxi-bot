# ==========================================
#   BOTNI ISHGA TUSHIRISH
# ==========================================

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import user, admin, group


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlar tartibi muhim emas, chunki admin routeri o'z ichida
    # ADMIN_ID bo'yicha filtrlangan — boshqa foydalanuvchilar avtomatik
    # ravishda keyingi routerga (user) o'tkaziladi.
    dp.include_router(admin.router)
    dp.include_router(group.router)
    dp.include_router(user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
