# Query the database to get all confirmed orders for each bot
# Save them in a file for each bot
from collections import defaultdict
import requests
import json
import time

import sys


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


def get_all_documents(COUCHDB_URL, DB_NAME, USERNAME, PASSWORD):
    # Get all documents in the database
    response = requests.get(
        f"{COUCHDB_URL}/{DB_NAME}/_all_docs?include_docs=true", auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()['rows']
    else:
        print(f"Error fetching documents: {response.json()}")
        return []


if __name__ == '__main__':
    db_ip = "database"
    COUCHDB_URL = f"http://{db_ip}:5984"
    USERNAME = "team"
    PASSWORD = "cloudcomputing"
    DB_NAME = "orders_database"

    net_position = defaultdict(int)
    total_profit = defaultdict(int)
    buy_qty = defaultdict(int)
    sell_qty = defaultdict(int)
    aggregated_data = defaultdict(list)

    documents = get_all_documents(COUCHDB_URL, USERNAME, PASSWORD, DB_NAME)
    for doc in documents:
        order = doc['doc']
        order_id = order['_id']
        order_type = order['type']
        quantity = order['quantity']
        price = order['price']
        bot = order_id.split("_")[0]

        if order_type == "buy":
            net_position[bot] += quantity  # Add to the position
            total_profit[bot] -= quantity * price
            buy_qty[bot] += quantity
            aggregated_data[bot].append({
                'id': order_id,
                'type': order_type,
                'quantity': quantity,
                'price': price,
                'profit': total_profit[bot] + net_position[bot] * price
            })
        elif order_type == "sell":
            net_position[bot] -= quantity  # Subtract from the position
            total_profit[bot] += quantity * price
            sell_qty[bot] += quantity
            aggregated_data[bot].append({
                'id': order_id,
                'type': order_type,
                'quantity': quantity,
                'price': price,
                'profit': total_profit[bot] + net_position[bot] * price
            })

    print(f"{'BOT':<10} {'PROFIT':<10} {'CURRENT POSITION':<20} {'TOTAL BUY QTY':<15} {'TOTAL SELL QTY':<15}")
    print("-" * 70)  # Dash line under the header

    for bot, aggr in aggregated_data.items():
        total_profit = aggr[-1]['profit']
        print(
            f"{bot:<10} {total_profit:<10} {net_position[bot]:<20} {buy_qty[bot]:<15} {sell_qty[bot]:<15}")
    # create_database(DB_NAME)
