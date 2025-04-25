import asyncio
from create_bot import bot, dp
from handlers.main_menu import menu_router

async def main() -> None:
    dp.include_router(menu_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
