import asyncio
import logging
import sys
from os import getenv
import requests
from aiogram import Bot, Dispatcher, Router, types 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command  
from aiogram.types import Message , CallbackQuery 
from aiogram.utils.markdown import hbold 
from aiogram.utils.keyboard import InlineKeyboardBuilder  , CallbackData , ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import F
from aiogram.types.keyboard_button_poll_type import KeyboardButtonPollType
from bot.callback_factory.callback import cb


backToMainMenu = InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data=cb(strt="tostart" , end=11).pack())
# start menu button 
startKeyboard = InlineKeyboardBuilder()
startKeyboard.button(text="💼 Manage Wallet" ,callback_data=cb(strt="Managewallet", end=11).pack())
startKeyboard.button(text="🛄 Claim" , callback_data=cb(strt="Claim", end=13).pack())
startKeyboard.adjust(2)

# wallet menu buttons 
def getWalletKeyboard(Has_wallet):
    walletdecisionkeyboard = InlineKeyboardBuilder()
    if Has_wallet:
        walletdecisionkeyboard.button(text="🗑 Delete Wallet" , callback_data=cb(strt="deletewallet" , end=11).pack())
        walletdecisionkeyboard.button(text="🏧 Widthraw Balance" , callback_data=cb(strt="widthdrawBalance" , end=111).pack())
        walletdecisionkeyboard.add(backToMainMenu)
        walletdecisionkeyboard.adjust(2,1)
    else:
        walletdecisionkeyboard.button(text="🔑 Generate New Wallet", callback_data=cb(strt="generate", end=12).pack())
        walletdecisionkeyboard.button(text="🔗 Connect Existing Wallet", callback_data=cb(strt="connect", end=13).pack())
        walletdecisionkeyboard.add(backToMainMenu)
        walletdecisionkeyboard.adjust(2,1)
    return walletdecisionkeyboard

# delete menu button 
deleteconfirmation = InlineKeyboardBuilder()
deleteconfirmation.button(text="✅ YES" , callback_data=cb(strt="yestodelete" , end=1).pack())
deleteconfirmation.button(text="❌ NO" , callback_data=cb(strt="Managewallet" , end=0).pack())
deleteconfirmation.button(text="BACK" , callback_data=cb(strt="Managewallet" , end=11).pack())
deleteconfirmation.adjust(2,1)

# deleletion confirmed now move to home 
backtotophome = InlineKeyboardBuilder()
backtotophome.add(backToMainMenu)


# wallet creation button 
