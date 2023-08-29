from bot.routers.routers import router
from aiogram.types import Message , CallbackQuery, ForceReply
from bot.callback_factory.callback import cb
from bot.db_client import db
from bot.keyboards.btn import *
from aiogram import F
from database.wallet_functions import user_has_wallet, add_wallet, delete_wallet_by_name, get_active_wallets
from bot.messages.messages import Welcome_Message, wallet_created, wallet_message
from bot.wallet_manager import WalletManager
from bot.wallets.wallet_handlers import eth_wm
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import re
# start with button 
@router.callback_query(cb.filter(F.strt == "tostart"))
async def Start(query : CallbackQuery)->None:
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(Welcome_Message , reply_markup=startKeyboard.as_markup())
  

# for claiming
@router.callback_query(cb.filter(F.strt == "Claim"))
async def claiming(query: CallbackQuery)->None:
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer("1):your not qualified to claim \n 2): you have claimed already \n 3): your claim is in process \n 4): you have successfully claimed)" , reply_markup=backtotophome.as_markup())

# for mananging the wallet 
@router.callback_query(cb.filter(F.strt == "Managewallet"))
async def Managewallet(query: CallbackQuery)->None:
    has_wallets = await user_has_wallet(query.from_user, db)
    wallet = None
    balance = None
    if has_wallets:
        wallet = await get_active_wallets(query.from_user, db)
        balance = eth_wm.get_balance(wallet.wallet_address)
    message = wallet_message(wallet=wallet, balance=balance)    
    walletkeyboard = getWalletKeyboard(has_wallets)
    await query.bot.delete_message(chat_id=query.message.chat.id ,message_id=query.message.message_id)
    await query.message.answer(message ,parse_mode="MARKDOWN", reply_markup=walletkeyboard.as_markup())


# for confirmation of  deleting the wallet 
@router.callback_query(cb.filter(F.strt == "deletewallet" ))
async def deletingtext(query:CallbackQuery):
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(f"Are you sure you want to delete you wallet ?" , reply_markup=deleteconfirmation.as_markup())

# wallet deletion confirmed 
@router.callback_query(cb.filter(F.strt == "yestodelete"))
async def walletdeletiondone(query:CallbackQuery):
    await delete_wallet_by_name(query.from_user, db)
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(f"Your wallet has been deleted" , reply_markup=backtotophome.as_markup())


# for creating the wallet 
@router.callback_query(cb.filter(F.strt == "generate"))
async def createwallet(query:CallbackQuery):
    wallet_data = {}
    seed, private, wallet = eth_wm.generate_new_address()
    wallet_data['encrypted_seed'] = eth_wm.encrypt_seed(private)
    wallet_data['address'] = wallet
    await add_wallet(query.from_user.id,wallet_data,db)
    message = wallet_created('ETH', wallet, private, seed)
    await query.bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer(message,parse_mode="MARKDOWN",reply_markup=backtotophome.as_markup())


# For connecting existing wwallet
@router.callback_query(cb.filter(F.strt == "connect"))
async def connect_existing_wallet_callback(query: types.CallbackQuery, state: FSMContext):
    await query.message.reply("Please enter your wallet private key:",reply_markup=ForceReply(input_field_placeholder="0x..../asjdh...."))
    await state.set_state('connect_existing_wallet')

@router.message(StateFilter('connect_existing_wallet'))
async def connect_existing_wallet_callback2(message: types.Message):
    
    address = message.text
    
    if not re.match("^(0x)?[0-9a-fA-F]{64}$", address):
        await message.reply("Invalid private key format. Please enter a valid private key.",reply_markup=backtotophome.as_markup())
        return


    if address.startswith("0x"):
        address = address[2:]
    wallet_data = {}
    
    
    wallet_data['encrypted_seed'] = eth_wm.encrypt_seed(address)
    wallet_data['address'] = eth_wm.get_eth_address(address)
    
    wallet = await add_wallet(message.from_user.id,wallet_data,db)
    
    
    # await update_user_holdT_status(user.chat_id, True, db)
    response = f'''✅ Added new wallet:\n\nChain: ETH \nAddress: `{wallet_data['address']}`\n\n'''
    await message.answer(response,parse_mode="MARKDOWN",reply_markup=backtotophome.as_markup())
