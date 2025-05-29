import telebot
import random
import threading
import time

API_TOKEN = '7842760543:AAHFbxnbifJYlGHWjTCfIgJVNfl_Dd7ttRM'
WALLET_ADDRESS = 'UQAnzg088aqSorf2rYteBGw6duFLYTR8VlxJv3QsXcALOKjP'

bot = telebot.TeleBot(API_TOKEN)

players = {}
levels = {}
nft_inventory = {}
fake_users = ['@MagicHero1', '@ElfQueen', '@DarkKnight', '@WizardMax', '@UndeadKing']
community_messages = [
    "🔥 {user} zdobył artefakt LEGENDARNY!",
    "💰 {user} zarobił już 5.2€ w grze!",
    "🏆 {user} pokonał dziś 12 potworów!",
    "⚔️ {user} wygrał pojedynek z przeciwnikiem PvP!",
    "🎉 {user} awansował na poziom 7 i dostał nowy NFT!"
]

@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    players[user_id] = {'hp': 100, 'level': 1}
    nft_inventory[user_id] = []
    bot.send_message(message.chat.id,
        "Welcome to Firos: Magic & Magic!\n"
        "Type /dungeon to fight, /pvp to duel, /buy to unlock, /nft to view your items or /top to see community.")

@bot.message_handler(commands=['dungeon'])
def dungeon(message):
    user_id = message.from_user.id
    if user_id not in players:
        bot.send_message(message.chat.id, "Use /start first!")
        return
    dmg = random.randint(5, 20)
    players[user_id]['hp'] -= dmg
    reward = random.randint(1, 3)
    levels[user_id] = levels.get(user_id, 0) + reward
    nft = f"NFT_Level_{levels[user_id]}"
    nft_inventory[user_id].append(nft)
    bot.send_message(message.chat.id,
        f"You fought in the dungeon and took {dmg} dmg.\n"
        f"You earned {reward} XP and received: {nft}")

@bot.message_handler(commands=['nft'])
def view_nft(message):
    user_id = message.from_user.id
    items = nft_inventory.get(user_id, [])
    if not items:
        bot.send_message(message.chat.id, "You have no NFTs yet. Fight in /dungeon!")
    else:
        bot.send_message(message.chat.id, "Your NFTs:\n" + "\n".join(items))

@bot.message_handler(commands=['pvp'])
def pvp(message):
    user_id = message.from_user.id
    opponent = random.choice(list(players.keys()) + fake_users)
    if opponent == user_id or len(players) < 1:
        bot.send_message(message.chat.id, "Not enough players for PvP.")
        return
    winner = random.choice([user_id, opponent])
    nft = f"NFT_PvP_Win_{random.randint(1, 100)}"
    if winner == user_id:
        players[user_id]['hp'] += 10
        nft_inventory[user_id].append(nft)
    bot.send_message(message.chat.id,
        f"You fought PvP vs {opponent}. Winner: {winner}\nNFT Reward: {nft if winner == user_id else 'None'}")

@bot.message_handler(commands=['buy'])
def send_payment_link(message):
    amount_eur = 2.00
    bot.send_message(message.chat.id,
        f"To unlock advanced missions or upgrade NFTs, pay {amount_eur} EUR via Tonkeeper:\n"
        f"https://tonkeeper.com/transfer/{WALLET_ADDRESS}?amount=200000000")

@bot.message_handler(commands=['top'])
def show_community(message):
    top_text = "🏅 Top Heroes in Firos:\n"
    for u in fake_users:
        top_text += f"{u} - lvl {random.randint(4, 15)}\n"
    bot.send_message(message.chat.id, top_text)

def fake_community_messages():
    while True:
        time.sleep(random.randint(120, 300))
        msg = random.choice(community_messages).format(user=random.choice(fake_users))
        bot.send_message(-1000000000000, msg)  # <- Zmień na ID Twojej grupy lub czatu

# Wątek do generowania fałszywych wiadomości
threading.Thread(target=fake_community_messages, daemon=True).start()

bot.infinity_polling()


from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Firos działa!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
