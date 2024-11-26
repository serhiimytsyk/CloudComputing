import requests
import json
import time

import sys
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer

db_ip = "database"
COUCHDB_URL = f"http://{db_ip}:5984"
USERNAME = "team"
PASSWORD = "cloudcomputing"

def database_exists(db_name):
    response = requests.get(f"{COUCHDB_URL}/{db_name}",
                            auth=(USERNAME, PASSWORD))
    return response.status_code == 200

def create_database(db_name):
    if not database_exists(db_name):
        response = requests.put(
            f"{COUCHDB_URL}/{db_name}", auth=(USERNAME, PASSWORD))
        if response.status_code == 201:
            print(f"Database '{db_name}' created successfully.")
        elif response.status_code == 412:
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Error creating database: {response.json()}")
    else:
        print(f"Database '{db_name}' already exists.")


def insert_document(db_name: str, doc: dict, action: str = "post") -> None:
    if action == "post":
        response = requests.post(
            f"{COUCHDB_URL}/{db_name}", json=doc, auth=(USERNAME, PASSWORD))
    else:
        get_response = requests.get(
            f"{COUCHDB_URL}/{db_name}/{doc['_id']}", auth=(USERNAME, PASSWORD))
        document: dict = get_response.json()
        document.update(doc)
        response = requests.put(
            f"{COUCHDB_URL}/{db_name}/{doc['_id']}", json=document, auth=(USERNAME, PASSWORD))

    if response.status_code in [201, 202]:
        print(f"Document inserted successfully: {response.json()}")
    else:
        print(f"Error inserting document: {response.json()}",
              f"status code: {response.status_code}")

# TODO Main logic has to be changed
# TODO We need to delete and create database again if it exists
# TODO Check if status is confirmed, ignore rejected orders
if __name__ == "__main__":
    DB_NAME = "orders_database"
    create_database(DB_NAME)

    consumer = KafkaConsumer(bootstrap_servers="kafka:9092")
    consumer.subscribe(topics=["orders_status"])
    for msg in consumer:
        document = json.loads(msg.value.decode('utf-8'))
        try:
            document['_id'] = str(document["id"])
            del document["id"]
            insert_document(DB_NAME, document, action="post")
            time.sleep(0.001)
        except KeyError:
            print("json object does not have _id key.")