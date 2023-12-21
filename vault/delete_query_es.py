import requests

# Elasticsearch endpoint
elasticsearch_url = "http://localhost:9200"

# Index and endpoint for delete by query
index_names = ["movie", "actor"]
for index in index_names:
    delete_by_query_endpoint = f"{elasticsearch_url}/{index}/_delete_by_query"

    # Query to match all documents
    query = {
        "query": {
            "match_all": {}
        }
    }

    # Send the POST request
    response = requests.post(delete_by_query_endpoint, json=query)

    # Check the response
    if response.status_code == 200:
        print("Documents deleted successfully.")
    else:
        print(f"Error: {response.status_code}, {response.text}")