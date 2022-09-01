import context

from framework.database import MongoDBConnection, MongoDBCursor


mongodb = MongoDBCursor(connector_object=MongoDBConnection())

print(mongodb.database)

list_collections = mongodb.get_collection_list()


result = mongodb.select_many({}, collection_name='crypto_currencies')

print(type(result))
for i in result:
    print(i["name"])

