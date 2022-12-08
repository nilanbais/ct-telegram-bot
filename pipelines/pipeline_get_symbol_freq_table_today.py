"""Getting tweets of the users in the database. It checks if a symbol ($) is present in the tweet

First draft of the pipeline is going to 
"""
import re
from typing import List, Dict

from pprint import pprint

import context
from framework.pipeline import Pipeline
from framework.twitter_api import TwitterAPI
from framework.api.communication import APICommunicator
from framework.database import MongoDBConnection, MongoDBCursor
from framework.text_analysis import CRYPTO_SYMBOL_REGEX_PATTERN
from framework.framework_utils.env_reader import EnvVarReader, RAPORTS_COLLECTION, USERS_COLLECTION


api = APICommunicator(TwitterAPI())
mongodb = MongoDBCursor(MongoDBConnection())

symbols_freq_table_today_pipeline = Pipeline()


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


@symbols_freq_table_today_pipeline.task()
def get_users_in_db() -> List[dict]:
    mongo_query = {}
    _result = mongodb.select_many(mongo_query, database_name=EnvVarReader().get_value("DB_DEFAULT_DATABASE"), collection_name=USERS_COLLECTION)
    return [obj["id"] for obj in _result]



@symbols_freq_table_today_pipeline.task(depends_on=get_users_in_db)
def get_symbolcount_per_user(input_list: List[dict]) -> List[dict]:
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


@symbols_freq_table_today_pipeline.task(depends_on=get_symbolcount_per_user)
def merge_freq_tables(freq_tables: Dict) -> dict:
    """"""
    the_table_of_all_tables = dict()
    for table in freq_tables.values():
        for key, value in table.items():
            if key in list(the_table_of_all_tables.keys()):
                old_val = the_table_of_all_tables[key]
                the_table_of_all_tables[key] = old_val + value
            else:
                the_table_of_all_tables[key] = value
    return the_table_of_all_tables


# @symbols_freq_table_today_pipeline.task(depends_on=merge_freq_tables)
def pprint_result(input_data: List[str]) -> None:
    """Pritty prints some shit
    """
    pprint(input_data)


symbols_freq_table_today_pipeline.run()