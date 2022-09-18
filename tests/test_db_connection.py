import context

from framework.database import MongoDBConnection, MongoDBCursor
from framework.framework_utils.env_reader import USERS_COLLECTION, RAPORTS_COLLECTION, CRYPTO_COLLECTION


mongodb = MongoDBCursor(connector_object=MongoDBConnection())

print(mongodb.database)

list_collections = mongodb.get_collection_list()


result = mongodb.select_many({}, collection_name=CRYPTO_COLLECTION)

print(type(result))
for i in result:
    print(i["name"])

