from jojo_es import * 
from jojo_janusgraph import * 
from jojo_mysql import * 

import threading 
import nest_asyncio

__all__ = [
    'get_or_create_es_connection',
    'get_or_create_janusgraph_connection', 
    'get_or_create_mysql_connection', 
]

_thread_local = threading.local()

nest_asyncio.apply()


def get_or_create_es_connection() -> ESClient:
    if getattr(_thread_local, 'es_client', None) is None:
        _thread_local.es_client = ESClient(host='192.168.0.83')
        
        print("[INFO] The connection to Elasticsearch is established.")

    return _thread_local.es_client


def get_or_create_janusgraph_connection() -> JanusGraphClient:
    if getattr(_thread_local, 'janusgraph_client', None) is None:
        _thread_local.janusgraph_client = JanusGraphClient('ws://192.168.0.83:8182/gremlin')
        
        print("[INFO] The connection to JanusGraph is established.")

    return _thread_local.janusgraph_client


def get_or_create_mysql_connection() -> MySQLClient:
    if getattr(_thread_local, 'mysql_client', None) is None:
        _thread_local.mysql_client = MySQLClient(
            host = '192.168.0.84', 
            user = 'root', 
            password = 'root', 
        )
        
        print("[INFO] The connection to MySQL is established.")

    return _thread_local.mysql_client
