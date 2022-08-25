import os

import telebot

import context
from framework.framework_utils.env_reader import EnvVarReader


API_TOKEN = EnvVarReader().get_value('BOT_HTTP_TOKEN')

bot = telebot.TeleBot(token=API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Whaddup famly, I'm under construction and not yet in use. Think of this as you personal safe space dude.")

@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message=message, text="What's good fam")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Not yet used ma boy")

bot.polling()