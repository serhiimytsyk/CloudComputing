import requests
import json
from kafka import KafkaConsumer  # consumer of events
consumer = KafkaConsumer (bootstrap_servers="localhost:9092")
# consumer.subscribe (topics=["utilizations"])
consumer.subscribe (topics=["images, prediction"])

# CouchDB configuration
db_ip = "127.0.0.1"
COUCHDB_URL = f"http://{db_ip}:5984"
USERNAME = "team"
PASSWORD = "cloudcomputing"

# Function to check if a database exists
def database_exists(db_name):
    response = requests.get(f"{COUCHDB_URL}/{db_name}", auth=(USERNAME, PASSWORD))
    return response.status_code == 200

# Function to create a database if it doesn't exist
def create_database(db_name):
    if not database_exists(db_name):
        response = requests.put(f"{COUCHDB_URL}/{db_name}", auth=(USERNAME, PASSWORD))
        if response.status_code == 201:
            print(f"Database '{db_name}' created successfully.")
        elif response.status_code == 412:
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Error creating database: {response.json()}")
    else:
        print(f"Database '{db_name}' already exists.")

# Function to insert a document
def insert_document(db_name, doc, action = "post"):
    if action == "post":
        response = requests.post(f"{COUCHDB_URL}/{db_name}", json=doc, auth=(USERNAME, PASSWORD))
    else:
        response = requests.put(f"{COUCHDB_URL}/{db_name}", json=doc, auth=(USERNAME, PASSWORD))

    if response.status_code in [201, 202]:
        print(f"Document inserted: {response.json()}")
    else:
        print(f"Error inserting document: {response.json()}")

# Main logic
if __name__ == "__main__":
    DB_NAME = "images_database"
    create_database(DB_NAME)

    for msg in consumer:
        if msg.topic == "image":
            document = json.load(msg.value.decode('utf-8'))
            try:
                document['_id'] = document["ID"]
                del document["ID"]
                insert_document(DB_NAME, document, action = "post")
            except KeyError:
                print("json object does not have _id key.")
        elif msg.topic == "prediction":
            document = json.load(msg.value.decode('utf-8'))
            try:
                document['_id'] = document["ID"]
                del document["ID"]
                insert_document(DB_NAME, document, action = "put")
            except KeyError:
                print("json object does not have _id key.")