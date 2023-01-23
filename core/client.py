import jojo_es 
import jojo_mysql 
import jojo_janusgraph 
import jojo_mongo 
import flask 
import threading 
from typing import Optional, Any 

__all__ = [
    'init_flask_client', 
    'get_es_client', 
    'get_mysql_client', 
    'get_janusgraph_client', 
    'get_mongo_client', 
]

flask_client_dict: dict[str, Any] = dict()
thread_local_client_dict = threading.local() 


def get_es_client() -> jojo_es.ESClient:
    try:
        return flask_client_dict['es_client']
    except KeyError:
        try:
            return thread_local_client_dict.es_client 
        except AttributeError:
            thread_local_client_dict.es_client = jojo_es.ESClient(
                host = '192.168.0.83', 
                port = 9200, 
            )
            return thread_local_client_dict.es_client 


def get_mysql_client() -> jojo_mysql.MySQLClient:
    try:
        return flask_client_dict['mysql_client']
    except KeyError:
        try:
            return thread_local_client_dict.mysql_client 
        except AttributeError:
            thread_local_client_dict.mysql_client = jojo_mysql.MySQLClient(
                host = '192.168.0.84', 
                port = 3306, 
                user = 'root', 
                password = 'root', 
            )
            return thread_local_client_dict.mysql_client 


def get_janusgraph_client() -> jojo_janusgraph.JanusGraphClient:
    try:
        return flask_client_dict['janusgraph_client']
    except KeyError:
        try:
            return thread_local_client_dict.janusgraph_client 
        except AttributeError:
            thread_local_client_dict.janusgraph_client = jojo_janusgraph.JanusGraphClient(
                url = 'ws://192.168.0.83:8182/gremlin', 
            )
            return thread_local_client_dict.janusgraph_client 


def get_mongo_client() -> jojo_mongo.MongoClient:
    try:
        return flask_client_dict['mongo_client']
    except KeyError:
        try:
            return thread_local_client_dict.mongo_client 
        except AttributeError:
            thread_local_client_dict.mongo_client = jojo_mongo.MongoClient(
                host = '192.168.0.86',
                port = 27017, 
            )
            return thread_local_client_dict.mongo_client 


def init_flask_client(flask_app: flask.Flask):
    es_client = jojo_es.ESClient(
        host = '192.168.0.83', 
        port = 9200, 
    )

    mysql_client = jojo_mysql.FlaskSQLAlchemyClient(
        host = '192.168.0.84', 
        port = 3306, 
        user = 'root', 
        password = 'root', 
    )

    janusgraph_client = jojo_janusgraph.JanusGraphClient(
        url = 'ws://192.168.0.83:8182/gremlin', 
    )

    mongo_client = jojo_mongo.FlaskPyMongoClient(
        host = '192.168.0.86',
        port = 27017, 
    )

    mysql_client.init_app(app=flask_app)
    mongo_client.init_app(app=flask_app)

    flask_client_dict['es_client'] = es_client 
    flask_client_dict['janusgraph_client'] = janusgraph_client 
    flask_client_dict['mongo_client'] = mongo_client 
    flask_client_dict['mysql_client'] = mysql_client 
