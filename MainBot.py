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
from bot.keyboards.btn import startKeyboard , walletdecisionkeyboard ,deleteconfirmation ,backtotophome
from bot.callback_factory.callback import cb
from bot.handlers.handlers import router
from dotenv import load_dotenv


load_dotenv()
TOKEN = getenv("TOKEN")

dp =  Dispatcher()


# for start command 
@router.message(CommandStart())
async def Start(message : Message )->None:
    await message.answer(f"🚀🎉 Hey there, Amazing Crypto Enthusiast! 🎉🚀\n"\

f"🔥 Welcome to the Unimix Token Reward Claiming Bot! 🔥\n"\

f"Hold onto your hats, because we've got some electrifying news for you. If you're the proud holder of Unimix tokens, you're in for a treat! 🎁💰 Get ready to claim Ethereum (ETH) like never before, simply by being a part of the Unimix token family.\n"\

f"💎 Your journey to claiming exciting rewards starts now. Fasten your seatbelt and follow the easy steps to unlock your ETH rewards. It's time to reap the benefits of your Unimix token ownership!\n"\

f"🌟 Don't wait a moment longer! Seize this golden opportunity to skyrocket your crypto adventure. Claim your ETH and watch your investments thrive.\n"\

f"Stay tuned for more updates, news, and thrilling opportunities coming your way through this bot. If you've got questions, we've got answers – simply drop us a message and our support team will be thrilled to assist you.\n"\

f"Let's make this crypto journey an unforgettable one – claim those rewards and conquer the world of Unimix tokens! 🌐🤖💰\n"\

f"To claim your rewards, click the button provided below and let the magic unfold! 🌈🚀\n"\

f"Happy claiming,\n"
f"The Unimix Token Team \n" , reply_markup=startKeyboard.as_markup())


async def main() -> None:

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
