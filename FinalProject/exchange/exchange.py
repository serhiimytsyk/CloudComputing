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

consumer = KafkaConsumer(bootstrap_servers="kafka:9092",
                         api_version=(0, 11, 5), consumer_timeout_ms = 15000)

time.sleep(30)

# Exchange state
# Read prepared data

def produce():
    time.sleep(0.001)
    pass # Send mid prices for each second in "prices" topic every second

def consume():
    consumer.subscribe(topics=["orders"])
    time.sleep(0.001)
    pass # Receive an order. If it matches the current state, send a confirmation, 
         # otherwise send a rejection into "orders_status" topic

if __name__ == "__main__":
    producer_thread = threading.Thread(target=produce)
    consumer_thread = threading.Thread(target=consume)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print("exchange done")