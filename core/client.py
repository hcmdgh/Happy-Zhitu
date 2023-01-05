import jojo_es 
import jojo_mysql 
import jojo_janusgraph 
import jojo_mongo 
import flask 
from typing import Optional, Any 

__all__ = [
    'init_client', 
    'get_es_client', 
    'get_mysql_client', 
    'get_janusgraph_client', 
    'get_mongo_client', 
]

es_client = None 
mysql_client = None 
janusgraph_client = None 
mongo_client = None 


def get_es_client() -> jojo_es.ESClient:
    return es_client  


def get_mysql_client() -> jojo_mysql.MySQLClient:
    return mysql_client


def get_janusgraph_client() -> jojo_janusgraph.JanusGraphClient:
    return janusgraph_client 


def get_mongo_client() -> jojo_mongo.MongoClient:
    return mongo_client 


def init_client(flask_app: Optional[flask.Flask] = None):
    global es_client, mysql_client, janusgraph_client, mongo_client 
    
    if flask_app is None:
        ESClient = jojo_es.ESClient
        MySQLClient = jojo_mysql.MySQLClient 
        JanusGraphClient = jojo_janusgraph.JanusGraphClient
        MongoClient = jojo_mongo.MongoClient
    else:
        ESClient = jojo_es.ESClient
        MySQLClient = jojo_mysql.FlaskSQLAlchemyClient 
        JanusGraphClient = jojo_janusgraph.JanusGraphClient
        MongoClient = jojo_mongo.FlaskPyMongoClient
        
    es_client = ESClient(
        host = '192.168.0.83', 
        port = 9200, 
    )

    mysql_client = MySQLClient(
        host = '192.168.0.84', 
        port = 3306, 
        user = 'root', 
        password = 'root', 
    )

    janusgraph_client = JanusGraphClient(
        url = 'ws://192.168.0.83:8182/gremlin', 
    )

    mongo_client = MongoClient(
        host = '192.168.0.86',
        port = 27017, 
    )

    if flask_app is not None:
        mysql_client.init_app(app=flask_app)
        mongo_client.init_app(app=flask_app)
