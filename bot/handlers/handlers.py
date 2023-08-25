from routers.routers import router
from aiogram.types import Message , CallbackQuery 
from callback_factory.callback import cb
from bot.db_client import db
from keyboards.btn import *
from aiogram import F
from database.wallet_functions import user_has_wallet
# start with button 
@router.callback_query(cb.filter(F.strt == "tostart"))
async def Start(query : CallbackQuery)->None:
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(f"🚀🎉 Hey there, Amazing Crypto Enthusiast! 🎉🚀\n"\

f"🔥 Welcome to the Unimix Token Reward Claiming Bot! 🔥\n"\

f"Hold onto your hats, because we've got some electrifying news for you. If you're the proud holder of Unimix tokens, you're in for a treat! 🎁💰 Get ready to claim Ethereum (ETH) like never before, simply by being a part of the Unimix token family.\n"\

f"💎 Your journey to claiming exciting rewards starts now. Fasten your seatbelt and follow the easy steps to unlock your ETH rewards. It's time to reap the benefits of your Unimix token ownership!\n"\

f"🌟 Don't wait a moment longer! Seize this golden opportunity to skyrocket your crypto adventure. Claim your ETH and watch your investments thrive.\n"\

f"Stay tuned for more updates, news, and thrilling opportunities coming your way through this bot. If you've got questions, we've got answers – simply drop us a message and our support team will be thrilled to assist you.\n"\

f"Let's make this crypto journey an unforgettable one – claim those rewards and conquer the world of Unimix tokens! 🌐🤖💰\n"\

f"To claim your rewards, click the button provided below and let the magic unfold! 🌈🚀\n"\

f"Happy claiming,\n"
f"The Unimix Token Team \n"  , reply_markup=startKeyboard.as_markup())
  

# for claiming
@router.callback_query(cb.filter(F.strt == "Claim"))
async def claiming(query: CallbackQuery)->None:
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer("1):your not qualified to claim \n 2): you have claimed already \n 3): your claim is in process \n 4): you have successfully claimed)" , reply_markup=backtotophome.as_markup())

# for mananging the wallet 
@router.callback_query(cb.filter(F.strt == "Managewallet"))
async def Managewallet(query: CallbackQuery)->None:
    has_wallets = await user_has_wallet(query.from_user, db)
    await query.bot.delete_message(chat_id=query.message.chat.id ,message_id=query.message.message_id)
    await query.message.answer(f"if your have wallet then select delete wallet \n if your don't have wallet click on create wallet \n " , reply_markup=walletdecisionkeyboard.as_markup())


# for confirmation of  deleting the wallet 
@router.callback_query(cb.filter(F.strt == "deletewallet" ))
async def deletingtext(query:CallbackQuery):
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(f"Are you sure you want to delete you wallet ?" , reply_markup=deleteconfirmation.as_markup())

# wallet deletion confirmed 
@router.callback_query(cb.filter(F.strt == "yestodelete"))
async def walletdeletiondone(query:CallbackQuery):
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(f"your account has been deleted! " , reply_markup=backtotophome.as_markup())


# for creating the wallet 
@router.callback_query(cb.filter(F.strt == "createwallet"))
async def createwallet(query:CallbackQuery):

    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(f"your wallet has been created! ")