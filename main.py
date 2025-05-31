import telebot

API_TOKEN = "YOUR_BOT_TOKEN"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Witaj w Firos: Magic & Magic!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "To tylko demo. Wersja gry wkrótce!")

bot.polling()
