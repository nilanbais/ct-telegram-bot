"""
"""
from typing import List

from pprint import pprint

import context

from framework.pipeline import Pipeline
from framework.coinmarketcap_api import CoinMarketCapAPI
from framework.api.communication import APICommunicator
from framework.database import MongoDBConnection, MongoDBCursor


api = APICommunicator(CoinMarketCapAPI())
mongodb = MongoDBCursor(MongoDBConnection())

update_crypto_symbols = Pipeline()


def get_cryptos_in_db():
    mongodb.select_many()


@update_crypto_symbols.task()
def get_a_fresh_list() -> List[dict]:

    result = api.connect_to_endpoint(endpoint='idmap')
    return result["data"]

@update_crypto_symbols.task(depends_on=get_a_fresh_list)
def clean_result(input_data: List[dict]) -> List[dict]:
    """Clean the input list based on sme specified keys to keep.
    """
    keys2keep = ["id", "name", "symbol"]
    
    raw_result = input_data
    clean_result = []
    for rresult in raw_result:
        clean_item = {key: rresult[key] for key in rresult.keys() if key in keys2keep}
        clean_result.append(clean_item)

    return clean_result


# @update_crypto_symbols.task(depends_on=clean_result)
# def pprint_result(input_data: List[dict]) -> None:
#     """Pritty prints some shit
#     """
#     pprint(input_data[:5])


@update_crypto_symbols.task(depends_on=clean_result)
def insert_list_into_db(input_list: List[dict], update_all:bool = False) -> None:

    if mongodb.select_one({}, collection_name='crypto_currencies') is None:
        print("going for insert")
        
        mongodb.insert_many(documents=input_list, database_name='cta-database', collection_name='crypto_currencies')
    else:
        print("going for update")

        if update_all:
            que = input_list.copy()
            for _ in range(len(input_list)):
                item = que[-1]
                query = {"name": item['name']}
                replace_val = {"$set": item}
                mongodb.update_one(query=(query, replace_val), collection_name='crypto_currencies')
                que.pop()
        else:
            result = mongodb.select_many({}, collection_name='crypto_currencies')
            symbols_in_db = [obj["symbol"] for obj in result]
            
            _to_do_list = [item for item in input_list if item["symbol"] not in symbols_in_db]

            keys_list =  ['id', 'name', 'symbol']
            to_do_list = [{key: item[key] for key in item.keys() if key in keys_list} for item in _to_do_list]
            # print(to_do_list)
            print("going add only new ones")

            if len(to_do_list) == 0:
                pass
            elif len(to_do_list) == 1:
                mongodb.insert_one(document=to_do_list, database_name='cta-database', collection_name='crypto_currencies')
            else:
                mongodb.insert_many(documents=to_do_list, database_name='cta-database', collection_name='crypto_currencies')

    print("done")




update_crypto_symbols.run()