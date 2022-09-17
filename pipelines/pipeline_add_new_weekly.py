"""
Scripts to add a new overview document of the past week.
Needs to be scheduled weekly, preferably sunday on monday.
"""
from datetime import datetime, timedelta
import re
from typing import List

from pprint import pprint

from pymongo.cursor import Cursor

import context

from framework.pipeline import Pipeline
from framework.database import MongoDBConnection, MongoDBCursor
from framework.framework_utils.env_reader import RAPORTS_COLLECTION


mongodb = MongoDBCursor(MongoDBConnection())

add_weekly_overview = Pipeline()

DAYS_TO_EXTRACT = [(datetime.today() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(7)]

@add_weekly_overview.task()
def get_data_from_db() -> list:
    """gets data of the past 7 days
    """
    print("Getting the last 7 daily report from the database")
    daily_raports = mongodb.select_many({"date": {"$in": DAYS_TO_EXTRACT}}, collection_name=RAPORTS_COLLECTION)
    return daily_raports

@add_weekly_overview.task(depends_on=get_data_from_db)
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
        "name": "Week Overview",
        "description": "A summary of the amount of times a crytpocurrency has been mentioned in a tweet in the focus group.",
        "interval": "Weekly",
        "week": datetime.today().strftime("%W"),
        "data": dict(sorted(week_data.items(), key=lambda item: item[-1], reverse=True))
    }
    return raport

@add_weekly_overview.task(depends_on=build_raport)
def insert_list_into_db(input_raport: List[dict]) -> None:
    print("Going to bring an updated weekly summary to the database")
    query = {"name": "Week Overview", "week": input_raport["week"]}
    weekly_overview_raport = mongodb.select_one(query, collection_name=RAPORTS_COLLECTION)
    if weekly_overview_raport is not None:
        print("gonna update the data")
        
        update_query = {"$set": {
            "data": input_raport["data"]
        }}
        mongodb.update_one(query=[query, update_query], collection_name=RAPORTS_COLLECTION)
    else:
        print("nothing found. dump it br")
        mongodb.insert_one(input_raport, collection_name=RAPORTS_COLLECTION)
    
    print("done")
    

add_weekly_overview.run()