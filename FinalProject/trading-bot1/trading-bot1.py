import os 
import time
import json
import sys

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

import random
import threading

import tensorflow as tf
import pandas as pd
import numpy as np

from kafka import KafkaProducer
from kafka import KafkaConsumer

producer = KafkaProducer(bootstrap_servers="kafka:9092",
                         acks=0,
                         api_version=(0, 11, 5))

consumer1 = KafkaConsumer(bootstrap_servers="kafka:9092",
                         api_version=(0, 11, 5), consumer_timeout_ms = 15000)

consumer2 = KafkaConsumer(bootstrap_servers="kafka:9092",
                         api_version=(0, 11, 5), consumer_timeout_ms = 150000)

time.sleep(30)

# Train a model
# Implement a state

def consume_prices():
    consumer1.subscribe(topics=["prices"])
    for msg in consumer1:
        time.sleep(0.001)
        pass # Get a price, make a prediction, send an order if we want

def consume_orders_status():
    consumer2.subscribe(topics=["orders_status"])
    for msg in consumer2:
        time.sleep(0.001)
        pass # Update the state

if __name__ == "__main__":
    thread1 = threading.Thread(target=consume_prices)
    thread2 = threading.Thread(target=consume_orders_status)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("trading bot 1 done")