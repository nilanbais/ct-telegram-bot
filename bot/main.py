"""


idee: een document waar ideeën voor rapportages verzameld kunnen worden.
"""
import os
from datetime import datetime, timedelta

import telebot

import context
from framework.framework_utils.env_reader import EnvVarReader

from framework.database import MongoDBConnection, MongoDBCursor


mongodb = MongoDBCursor(MongoDBConnection())


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

@bot.message_handler(commands=['today'])
def today(message):
    raw_data = mongodb.select_one(mongodb_query={"date": datetime.today().strftime('%Y-%m-%d')}, collection_name='raports')
    data = {key: value for key, value in raw_data.items() if key != '_id'}
    newline = '\n'
    tab = '\t'

    text = f"""
    
What is up. I've got one daily report for U, my friend

{'-' * 20}
{data['name']}
{data["description"]}
The date is {data['date']}

{newline.join([f"{key}{tab * 2}{val}" for key, val in data['data'].items()])}

tenk U come again
    """
    bot.reply_to(message=message, text=text)

@bot.message_handler(commands=['yesterday'])
def yesterday(message):
    yesterday_date = datetime.today() - timedelta(days=1)
    raw_data = mongodb.select_one(mongodb_query={"date": yesterday_date.strftime('%Y-%m-%d')}, collection_name='raports')
    data = {key: value for key, value in raw_data.items() if key != '_id'}
    newline = '\n'
    tab = '\t'

    text = f"""
    
What is up. I've got one daily report for U, my friend

{'-' * 20}
{data['name']}
{data["description"]}
The date is {data['date']}

{newline.join([f"{key}{tab * 2}{val}" for key, val in data['data'].items()])}

tenk U come again
    """
    bot.reply_to(message=message, text=text)


bot.polling() 