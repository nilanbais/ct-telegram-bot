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

USERS_COLLECTION = EnvVarReader().get_value('DB_USERS_COLLECTION')
CRYPTO_COLLECTION = EnvVarReader().get_value('DB_CRYPTO_COLLECTION')
REPORTS_COLLECTION = EnvVarReader().get_value('DB_RAPORTS_COLLECTION')

bot = telebot.TeleBot(token=API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    t = """crypto_twitter_analysis_bot OUT NOW go and chat with the one and only best there is crypto bot for things you know I know so let's stop talking and go get this goldendrop on a tuesday morning type ass motherf*cker skrt what's good"""
    extrended_t = t + '\n' + """
/start
/today
/yesterday
/last_week
    """
    bot.send_message(message.chat.id, extrended_t)

@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message=message, text="What's good fam")

@bot.message_handler(commands=['help', 'menu'])
def help(message):
    t = """
/start
/today
/yesterday
/last_week
    """
    bot.send_message(message.chat.id, text=t)

@bot.message_handler(commands=['today'])
def today(message):
    raw_data = mongodb.select_one(mongodb_query={"date": datetime.today().strftime('%Y-%m-%d')}, collection_name=REPORTS_COLLECTION)
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
    raw_data = mongodb.select_one(mongodb_query={"date": yesterday_date.strftime('%Y-%m-%d')}, collection_name=REPORTS_COLLECTION)
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


@bot.message_handler(commands=['last_week'])
def last_week(message):
    raw_data = mongodb.select_one(mongodb_query={"name": "Weekly Summary"}, collection_name=REPORTS_COLLECTION)
    data = {key: value for key, value in raw_data.items() if key != '_id'}
    newline = '\n'
    tab = '\t'

    text = f"""
    
What is up. I've got one summary of last week for ypu, my friend

{'-' * 20}
{data['name']}
{data["description"]}
The dates summed up are: {data['days']}

{newline.join([f"{key}{tab * 2}{val}" for key, val in data['data'].items()])}

Thank you come again
    """
    bot.reply_to(message=message, text=text)


if __name__ == '__main__':
    print("crypto_twitter_analysis_bot OUT NOW go to telegram to chat with the one and only best there is crypto bot for things you know I know so let's stop talking and go get this goldendrop on a tuesday morning type ass motherf*cker skrt what's good")
    bot.polling()