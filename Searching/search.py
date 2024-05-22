import pysolr
import json

import time

# Configuration
solr_url = 'http://localhost:8983/solr'  # Replace with your Solr URL
collection_name = 'nela-2021'

# Initialize Solr connection
solr = pysolr.Solr(f'{solr_url}/{collection_name}', always_commit=True, timeout=10)

# Create the collection (this step assumes you have access to Solr's API to create collections)
def create_collection():
    import requests
    params = {
        'action': 'CREATE',
        'name': collection_name,
        'numShards': 1,
        'replicationFactor': 1,
        'wt': 'json'
    }
    response = requests.get(f'{solr_url}/admin/collections', params=params)
    print(f'Collection creation response: {response.json()}')
    time.sleep(5)  # Give some time for the collection to be created

# Add documents
def add_documents():
    documents = [
        {'id': '1', 'title': 'First Document', 'content': 'This is the first document'},
        {'id': '2', 'title': 'Second Document', 'content': 'This is the second document'},
        {'id': '3', 'title': 'Third Document', 'content': 'This is the third document'},
    ]
    solr.add(documents)
    print('Documents added successfully.')

# Query Documents
def query_documents(query):
    solr_url = 'http://localhost:8983/solr'  # Replace with your Solr URL
    collection_name = 'nela-2021'

    solr = pysolr.Solr(f'{solr_url}/{collection_name}', always_commit=True, timeout=10)

    results = solr.search("*:*", rows=10)  # Adjust 'rows' to get more or fewer results

    return results

if __name__ == '__main__':
    query_documents('*:*')

