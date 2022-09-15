"""Add report to database of the data seen today.
"""
from datetime import date, datetime
import re
from typing import List, Dict, Optional

from pprint import pprint

import context

from framework.pipeline import Pipeline
from framework.coinmarketcap_api import CoinMarketCapAPI
from framework.api.communication import APICommunicator
from framework.database import MongoDBConnection, MongoDBCursor

from framework.text_analysis import CRYPTO_SYMBOL_REGEX_PATTERN
from framework.twitter_api import TwitterAPI



mongodb = MongoDBCursor(MongoDBConnection())

update_daily_report = Pipeline()



def get_symbols_from_tweet(input_string: str) -> list:
    return re.findall(CRYPTO_SYMBOL_REGEX_PATTERN, input_string)


def get_symbol_freq_table(input_list: List[list]) -> dict:
    freq_table = dict()
    for item in input_list:
        _crypto_symbols = re.findall(CRYPTO_SYMBOL_REGEX_PATTERN, item)        
        for symbol in _crypto_symbols:
            if symbol in freq_table.keys():
                freq_table[symbol] = freq_table[symbol] + 1
            else:
                freq_table[symbol] = 1
    return freq_table


def get_a_fresh_list() -> List[dict]:
    api = APICommunicator(CoinMarketCapAPI())
    result = api.connect_to_endpoint(endpoint='idmap')
    raw_result = result["data"]

    keys2keep = ["id", "name", "symbol"]   
    clean_result = []
    for rresult in raw_result:
        clean_item = {key: rresult[key] for key in rresult.keys() if key in keys2keep}
        clean_result.append(clean_item)

    return clean_result
    


@update_daily_report.task()
def get_users_in_db() -> List[dict]:
    print("Getting the users from the database.")
    mongo_query = {}
    _result = mongodb.select_many(mongo_query, database_name='cta-database', collection_name='users')
    return [obj["id"] for obj in _result]



@update_daily_report.task(depends_on=get_users_in_db)
def get_symbolcount_per_user(input_list: List[dict]) -> List[dict]:
    print("Counting the crypto symbols metioned per user")
    api = APICommunicator(TwitterAPI())
    header = {"User-Agent": "v2UserTweetsPython"}
    qp = {"tweet.fields": "created_at"}

    tweet_info = dict()
    for user_id in input_list:
        result = api.connect_to_endpoint(endpoint='user_tweets', header_kwargs=header, query_parameters_kwargs=qp, user_id=user_id)
        if len(result) == 1:
            continue

        clean_list = [obj['text'] for obj in result['data']]

        freq_table = get_symbol_freq_table(input_list=clean_list)

        if len(freq_table.keys()) > 0:
            tweet_info[user_id] = freq_table
        
    return tweet_info


@update_daily_report.task(depends_on=get_symbolcount_per_user)
def merge_freq_tables(freq_tables: Dict) -> dict:
    """"""
    print("Going to merge the counts from previous task")
    the_table_of_all_tables = dict()
    for table in freq_tables.values():
        for key, value in table.items():
            if key in list(the_table_of_all_tables.keys()):
                old_val = the_table_of_all_tables[key]
                the_table_of_all_tables[key] = old_val + value
            else:
                the_table_of_all_tables[key] = value
    return the_table_of_all_tables


def get_currency_name(symbol: str, search_list: List[dict]) -> Optional[str]:
    for item in search_list:
        if item["symbol"] == symbol:
            return item["name"]


@update_daily_report.task(depends_on=merge_freq_tables)
def build_raport(freq_table: dict) -> dict:
    print("Building the raport")
    fresh_symbol_summary = get_a_fresh_list()
    data_object = dict()
    for key, value in freq_table.items():
        _symbol = key.replace('$', '')
        name = get_currency_name(_symbol, fresh_symbol_summary)
        if name is None:
            name = key
        data_object[name] = value

    raport = {
        "name": "Daily Summary",
        "description": "A summary of the amount of times a crytpocurrency has been mentioned in a tweet in the focus group.",
        "interval": "daily",
        "date": datetime.today().strftime('%Y-%m-%d'),
        "data": dict(sorted(data_object.items(), key=lambda item: item[1], reverse=True))
    }
    return raport


@update_daily_report.task(depends_on=build_raport)
def insert_list_into_db(input_raport: List[dict]) -> None:
    print("Going to bring a fresh fresh result to the database")
    daily_raport = mongodb.select_one({"date": datetime.today().strftime('%Y-%m-%d')}, collection_name='raports')
    if daily_raport is not None:
        print("gonna update the data")
        query = {"date": daily_raport["date"]}
        update_query = {"$set": {
            "data": input_raport["data"]
        }}
        mongodb.update_one(query=[query, update_query], collection_name='raports')
    else:
        print("nothing found. dump it br")
        mongodb.insert_one(input_raport, collection_name='raports')
    
    print("done")


update_daily_report.run()