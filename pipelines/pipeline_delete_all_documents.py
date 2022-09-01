



from tkinter import Y
import context

from framework.pipeline import Pipeline
from framework.twitter_api import TwitterAPI
from framework.api.communication import APICommunicator
from framework.database import MongoDBConnection, MongoDBCursor



pipeline = Pipeline()

api = APICommunicator(TwitterAPI())
mongodb = MongoDBCursor(MongoDBConnection())



@pipeline.task()
def delete_users()-> None:
    mongodb._empty_collection(collection_name='users')

pipeline.run()