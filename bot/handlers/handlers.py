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
async def connect_existing_wallet_callback(query: types.CallbackQuery):
    await query.reply("Please enter your wallet private key:",reply_markup=ForceReply(input_field_placeholder="0x..../asjdh...."))

@router.message(StateFilter(WalletState.connect_wallet))
async def connect_existing_wallet_callback2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    network = data.get("network")
    address = message.text
    
    if not re.match("^(0x)?[0-9a-fA-F]{64}$", address):
        await message.reply("Invalid private key format. Please enter a valid private key.",reply_markup=back_to_main_kb())
        await state.set_state(None)
        return


    if address.startswith("0x"):
        address = address[2:]
    wallet_data = {}
    
    
    wallet_data['encrypted_seed'] = eth_test_wm.encrypt_seed(address)
    wallet_data['name'] = data['wallet_name']
    wallet_data['address'] = eth_test_wm.get_eth_address(address)
    wallet_data['network'] = network
    
    wallet = await add_wallet(message.from_user.id,wallet_data,db)
    if network == "ethereum":
        settings_data = default_eth_settings
    elif network == "bsc":
        settings_data = default_bsc_settings
    else:
        settings_data = default_arb_settings
    await add_user_settings(message.from_user, settings_data, db)
    user = await get_user_by_chat_id(message.from_user.id, db)
    status = ""
    if not (user.paid or user.holds_token) and "eth" in network:
        wallet_address = wallet_data['address']
        eth_uni_m.address = eth_uni_m.w3.to_checksum_address(wallet_address) 
        balance = eth_uni_m.get_token_balance(eth_uni_m.w3.to_checksum_address(HOLDING_TOKEN_ADDRESS))
        balance = eth_uni_m.w3.from_wei(balance,"ether")
        
        if balance>=HOLDING_QUANTITY:
            data = {
            "wallet_address": wallet.wallet_address,
            "timestamp": datetime.datetime.now(),
            "token_address": HOLDING_TOKEN_ADDRESS,
            "amount" : HOLDING_QUANTITY,
            "tx_hash": "0x"
            }
            await add_holding_buy(user.chat_id, data, db)
            # await update_user_holdT_status(user.chat_id, True, db)
            status = f"🎉 Good news! It seems that your wallet already holds {HOLDING_QUANTITY} of {HOLDING_TOKEN_NAME} 🪙, meeting our criteria 📋. Now, you can enjoy full access to all the amazing features of the bot 🤖! Happy trading 📈 and make the most out of it! 😃🚀"
    response = f'''✅ Added new wallet:\n\nName: {wallet_data['address']}\nChain: {network}\nAddress: `{wallet_data['address']}`\n\n{status}'''
    await message.answer(response,parse_mode="MARKDOWN",reply_markup=back_to_main_kb())
    await state.set_state(None)
