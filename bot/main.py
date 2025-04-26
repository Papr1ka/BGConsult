import asyncio
from .handlers.main_menu import menu_router
from .create_bot import (
    cfg,
    ParseMode,
    DefaultBotProperties,
    Bot,
    Dispatcher,
    MemoryStorage,
)


async def main() -> None:
    dp.include_router(menu_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    bot = Bot(token=cfg.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    asyncio.run(main())
