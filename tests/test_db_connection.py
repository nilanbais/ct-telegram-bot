import context

from framework.database import MongoDBConnection, MongoDBCursor


mongodb = MongoDBCursor(connector_object=MongoDBConnection())

print(mongodb.database)

list_collections = mongodb.get_collection_list()

[print(mongodb.select_one({}, collection_name=col_names)) for col_names in list_collections]