import jojo_es 
import jojo_mysql 
import jojo_janusgraph 
import jojo_mongo 

__all__ = [
    'es_client', 
    'mysql_client', 
    'janusgraph_client', 
    'mongo_client', 
]

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
