import asyncio
import logging
import sys
from os import getenv
import requests
from aiogram import Bot, Dispatcher, types 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command  
from aiogram.types import Message , CallbackQuery 
from aiogram.utils.markdown import hbold 
from aiogram.utils.keyboard import InlineKeyboardBuilder  , CallbackData , ReplyKeyboardBuilder
from aiogram import F
from aiogram.types.keyboard_button_poll_type import KeyboardButtonPollType
from bot.keyboards.btn import startKeyboard 
from bot.callback_factory.callback import cb
from bot.handlers.handlers import router
from bot.Middlewares.user_middleware import UserCheckMiddleware
from dotenv import load_dotenv
from bot.messages.messages import Welcome_Message

load_dotenv()
TOKEN = getenv("TOKEN")

dp =  Dispatcher()


# for start command 
@router.message(CommandStart())
async def Start(message : Message )->None:
    await message.answer(Welcome_Message , reply_markup=startKeyboard.as_markup())


async def main() -> None:

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.message.middleware(UserCheckMiddleware())
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
