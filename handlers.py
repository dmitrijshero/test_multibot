from aiogram import Dispatcher, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import config
from states import UserStates
from aiogram.filters import CommandStart
from aiogram.utils.markdown import html_decoration as fmt
from aiogram.utils.token import TokenValidationError
from polling_manager import PollingManager


async def start(message: Message, state: FSMContext):
    await message.answer("Введите токен нового бота")
    await state.set_state(UserStates.InputToken)


async def get_new_token(message: Message, state: FSMContext, polling_manager: PollingManager):
    token = message.text
    if token == config.TOKEN:
        await message.answer("Этот бот уже был запущен ранее. Введите другой токен")
        return

    try:
        bot = Bot(token)

    except TokenValidationError as err:
        await message.answer(fmt.quote(f"{type(err).__name__}: {str(err)}"))
        return

    await state.set_state(UserStates.Normal)
    new_dp = Dispatcher()
    polling_manager.start_bot_polling(
        dp=new_dp,
        bot=bot,
        polling_manager=polling_manager,
        dp_for_new_bot=new_dp,
    )
    bot_user = await bot.get_me()
    await message.answer(f"New bot started: @{bot_user.username}")
    new_dp.message.register(message_handler)


async def message_handler(message: Message):
    await message.answer(f"Привет. Твое сообщение: {message.text}")


routers = []
main_router = Router()
main_router.message.register(start, CommandStart())
main_router.message.register(get_new_token, UserStates.InputToken)
polling_manager = PollingManager()
