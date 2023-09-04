Welcome_Message = f'''🚀🎉 Hey there, Amazing Crypto Enthusiast! 🎉🚀\n\

🔥 Welcome to the Unimix Token Reward Claiming Bot! 🔥\n\

Hold onto your hats, because we've got some electrifying news for you. If you're the proud holder of Unimix tokens, you're in for a treat! 🎁💰 Get ready to claim Ethereum (ETH) like never before, simply by being a part of the Unimix token family.\n\

💎 Your journey to claiming exciting rewards starts now. Fasten your seatbelt and follow the easy steps to unlock your ETH rewards. It's time to reap the benefits of your Unimix token ownership!\n\

🌟 Don't wait a moment longer! Seize this golden opportunity to skyrocket your crypto adventure. Claim your ETH and watch your investments thrive.\n\

Stay tuned for more updates, news, and thrilling opportunities coming your way through this bot. If you've got questions, we've got answers – simply drop us a message and our support team will be thrilled to assist you.\n\

Let's make this crypto journey an unforgettable one – claim those rewards and conquer the world of Unimix tokens! 🌐🤖💰\n\

To claim your rewards, click the button provided below and let the magic unfold! 🌈🚀\n\

Happy claiming,\n
The Unimix Token Team \n'''

def wallet_message(wallet,balance):
    if wallet:
        message = f'''🔗 *Network:* ETH\n
                      💰 *Available Balance:* {balance} *ETH*\n
                      📬 *Wallet Address:* `{wallet.wallet_address}`\n\n"'''
    else:
        message = f'''Pepetricia’s Sniperbot 💕 🐸  

🚫👛 Oh no! It looks like you don't have an ETH wallet set up yet. 🤔
💼 Before diving deep into the token pool or making payments, you'll need to set up your ETH wallet. 🌊💸
🚀 Ready to take the plunge? Set up your wallet and let's get sniping! 🎯🐸'''
    return message

def wallet_created(*args):
    Wallet_Created_Message = f'''✅ Generated new wallet:\n
                                 🌐 Chain: {args[0]}\n
                                 📬 Address:\n `{args[1]}`\n
                                 🔑 Private Key:\n `{args[2]}`\n
                                 🧠 Mnemonic Phrase:\n `{args[3]}`

    ⚠️ Make sure to save this mnemonic phrase OR private key using pen and paper only. Do NOT copy-paste it anywhere. You could also import it to your Metamask/Trust Wallet. After you finish saving/importing the wallet credentials, delete this message. The bot will not display this information again.'''
    return Wallet_Created_Message

def ifClaim(claimed):
    if not claimed:
        message = f'''Pepetricia’s Sniperbot 💕 🐸  

🚫👛 Oh no! It looks like you can not claim yet. 🤔
💼 Before claiming make sure the following : 
    1. You cannot reclaim within 24 hours so have patience my child. 🌊🐸🎯🚀'''

    else:
        message = f'''Pepetricia’s Sniperbot 💕 🐸  

✅ Great! Your transaction is initiated you'll be notified soon . 🎉💸
💼 Before claiming make sure the followings : 
    1. If you are not a holder then let's buy some XYZ token to claim reward. 🌊🐸🎯'''