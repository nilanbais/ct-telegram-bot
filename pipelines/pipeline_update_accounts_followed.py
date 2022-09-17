"""
Script to update the list of users in the database.
There is not yet a concrete strategy to manage the users in the database.
"""
from typing import List
from pprint import pprint

import context

from framework.pipeline import Pipeline
from framework.twitter_api import TwitterAPI
from framework.api.communication import APICommunicator
from framework.database import MongoDBConnection, MongoDBCursor
from framework.framework_utils.env_reader import RAPORTS_COLLECTION




pipeline = Pipeline()

api = APICommunicator(TwitterAPI())
mongodb = MongoDBCursor(MongoDBConnection())


@pipeline.task()
def get_account_list() -> list:

    header = {"User-Agent": "v2FollowingLookupPython"}
    qp = {"user.fields": "public_metrics"}
    result = api.connect_to_endpoint(endpoint='following', header_kwargs=header, query_parameters_kwargs=qp)
    return result['data']

@pipeline.task(depends_on=get_account_list)
def clean_list(input_list: List[dict]) -> List[dict]:
        """Changes the dicts in the list of accounts followed by the base_user, to keep
        the id, username, name, and followers_count.
        """
        result_list = list()
        for item in input_list:
            public_metrics = item["public_metrics"]
            result_list.append({
                "id": item["id"],
                "username": item["username"],
                "name": item["name"],
                "followers_count": public_metrics["followers_count"]
            })
        return result_list

@pipeline.task(depends_on=clean_list)
def print_result(input_data):
    pprint(input_data)

@pipeline.task(depends_on=clean_list)
def insert_list_into_db(input_list: List[dict]) -> None:

    if mongodb.select_one({}, collection_name=RAPORTS_COLLECTION) is None:
        print("going for insert")
        
        mongodb.insert_many(documents=input_list, database_name='cta-database', collection_name=RAPORTS_COLLECTION)

    else:
        print("going for update")

        que = input_list.copy()
        for _ in range(len(input_list)):
            item = que[-1]
            query = {"name": item['name']}
            replace_val = {"$set": item}
            mongodb.update_one(query=(query, replace_val), collection_name=RAPORTS_COLLECTION)
            que.pop()
            print(len(que))
        
        if len(que) > 0:
            print("going for aditional insert")
            mongodb.insert_many(documents=que, database_name='cta-database', collection_name=RAPORTS_COLLECTION)

    print("done")

pipeline.run()