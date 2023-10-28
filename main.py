import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

import config
import handlers


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="start"),
        BotCommand(command="stop", description="stop")
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.main_router)
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=False, polling_manager=handlers.polling_manager)


if __name__ == "__main__":
    asyncio.run(main())
