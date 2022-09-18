"""
Scripts to add a new overview document of the past month.
Needs to be scheduled monthly, preferably sunday on monday.
"""
from datetime import date, datetime, timedelta
import re
from typing import List

from pprint import pprint

from pymongo.cursor import Cursor

import context

from framework.pipeline import Pipeline
from framework.database import MongoDBConnection, MongoDBCursor
from framework.framework_utils.env_reader import RAPORTS_COLLECTION

mongodb = MongoDBCursor(MongoDBConnection())

add_monthly_overview = Pipeline()


LAST_MONTH_LAST_DAY = date.today().replace(day=1) - timedelta(days=1)
DAYS_TO_EXTRACT = [(date.today().replace(day=1) - timedelta(days=x)) for x in range(40) if (date.today().replace(day=1) - timedelta(days=x)).strftime("%m") == LAST_MONTH_LAST_DAY.strftime("%m")]  # gets list of dates of ther past month

@add_monthly_overview.task()
def get_data_from_db() -> list:
    """gets data of the past 4 weeks
    """
    print("Getting the last 7 daily report from the database")
    query = {"name": "Daily Summary", "date": {"$in": DAYS_TO_EXTRACT}}
    daily_raports = mongodb.select_many(query, collection_name=RAPORTS_COLLECTION)
    return daily_raports

@add_monthly_overview.task(depends_on=get_data_from_db)
def build_raport(mongo_cursor: Cursor) -> dict:
    """sums the data in the queried documents
    """
    print("Raport under construction. Please put on your helmet")
    month_data = dict()
    for record in mongo_cursor:
        _data = record['data']
        for key, value in _data.items():
            if key in list(month_data.keys()):
                month_data[key] += value
            else:
                month_data[key] = value

    raport = {
        "name": "Month Overview",
        "description": "A summary of the amount of times a crytpocurrency has been mentioned in a tweet in the focus group.",
        "interval": "Monthly",
        "month": LAST_MONTH_LAST_DAY.strftime("%M"),
        "data": dict(sorted(month_data.items(), key=lambda item: item[-1], reverse=True))
    }
    return raport

@add_monthly_overview.task(depends_on=build_raport)
def insert_list_into_db(input_raport: List[dict]) -> None:
    print("Going to bring an updated weekly summary to the database")
    query = {"name": "Month Overview", "month": input_raport["month"]}
    monthly_overview_raport = mongodb.select_one(query, collection_name=RAPORTS_COLLECTION)
    if monthly_overview_raport is not None:
        print("gonna update the data")
        
        update_query = {"$set": {
            "data": input_raport["data"]
        }}
        mongodb.update_one(query=[query, update_query], collection_name=RAPORTS_COLLECTION)
    else:
        print("nothing found. dump it br")
        mongodb.insert_one(input_raport, collection_name=RAPORTS_COLLECTION)
    
    print("done")
    

add_monthly_overview.run()