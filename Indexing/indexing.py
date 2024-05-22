import requests
import pysolr
import json
import os

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
def add_documents(path_to_file_directories):
    documents = []

    for file in os.listdir(path_to_file_directories):
        with open(f"{path_to_file_directories}/{file}", 'r') as fh:
            articles = json.load(fh)
    for article in articles:
        documents.append(article)
        # print(article)

    solr.add(documents)
    print('Documents added successfully.')

# Query documents
# Query documents
def query_documents(query_string):
    print("Searching for documents:")
    results = solr.search(query_string)
    print(f'Found {len(results)} document(s).')
    for result in results:
        print(f' - {result["id"]}: {result["title"]}')

if __name__ == '__main__':
    # create_collection()
    add_documents('data/nela-gt-2021/newsdata/test')
    
    
    # query_string = '"Germany Drought Ends"'  # Query string for the phrase
    # query_documents(query_string)
