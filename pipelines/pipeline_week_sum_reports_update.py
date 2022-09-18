"""
The report gets updated daily and sums up the data of the last week.
Needs to be scheduled daily.
"""
from datetime import date, datetime, timedelta
import re
from typing import List, Dict, Optional

from pprint import pprint

from pymongo.cursor import Cursor

import context

from framework.pipeline import Pipeline
from framework.coinmarketcap_api import CoinMarketCapAPI
from framework.api.communication import APICommunicator
from framework.database import MongoDBConnection, MongoDBCursor

from framework.text_analysis import CRYPTO_SYMBOL_REGEX_PATTERN
from framework.twitter_api import TwitterAPI



mongodb = MongoDBCursor(MongoDBConnection())

update_week_sum = Pipeline()

DAYS_TO_EXTRACT = [(datetime.today() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(7)]

@update_week_sum.task()
def get_data_from_db() -> list:
    """gets data of the past 7 days
    """
    print("Getting the last 7 daily report from the database")
    daily_raports = mongodb.select_many({"date": {"$in": DAYS_TO_EXTRACT}}, collection_name='raports')
    return daily_raports

@update_week_sum.task(depends_on=get_data_from_db)
def build_raport(mongo_cursor: Cursor) -> dict:
    """sums the data in the queried documents
    """
    print("Raport under construction. Please put on your helmet")
    week_data = dict()
    for record in mongo_cursor:
        _data = record['data']
        for key, value in _data.items():
            if key in list(week_data.keys()):
                week_data[key] += value
            else:
                week_data[key] = value

    raport = {
        "name": "Weekly Summary",
        "description": "A summary of the amount of times a crytpocurrency has been mentioned in a tweet in the focus group.",
        "interval": "Weekly",
        "days": ", ".join(DAYS_TO_EXTRACT),
        "data": dict(sorted(week_data.items(), key=lambda item: item[-1], reverse=True))
    }
    return raport

@update_week_sum.task(depends_on=build_raport)
def insert_list_into_db(input_raport: List[dict]) -> None:
    print("Going to bring an updated weekly summary to the database")
    query = {"name": "Weekly Summary"}
    weekly_raport = mongodb.select_one(query, collection_name='raports')
    if weekly_raport is not None:
        print("gonna update the data")
        
        update_query = {"$set": {
            "days": input_raport["days"],
            "data": input_raport["data"]
        }}
        mongodb.update_one(query=[query, update_query], collection_name='raports')
    else:
        print("nothing found. dump it br")
        mongodb.insert_one(input_raport, collection_name='raports')
    
    print("done")
    

update_week_sum.run()