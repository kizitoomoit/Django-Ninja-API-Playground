
from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch("http://localhost:9200")

# Test connection
if es.ping():
    print("Elasticsearch is ready!")
else:
    print("Cannot connect to Elasticsearch")