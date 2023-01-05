import jojo_es

__all__ = [
    'google_es_client', 
    'google_author_index',
    'google_paper_index', 
]

google_es_client = jojo_es.ESClient(
    host = '192.168.0.90',
    port = 9200, 
)

google_author_index = google_es_client.get_index('google_author', type_name='doc')
google_paper_index = google_es_client.get_index('google_paper', type_name='doc')
