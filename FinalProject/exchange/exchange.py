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

prices = []
with open('./2024-11-20.txt', 'r') as file:
    content = file.read()
    prices = list(map(float, content.split()))

delta = 0.001
eps = 0.00001
current_index = 0

def send_order_status(id, status, type, quantity, price):
    status = {
        'id': id,
        'status': status,
        'type': type,
        'quantity': quantity,
        'price': price
    }
    status = json.dumps(status)
    producer.send(topic = 'orders_status', value = status.encode('utf-8'))
    producer.flush()

time.sleep(30)

def produce():
    for i in range(len(prices)):
        current_index = i
        price_info = {
            'price': prices[i]
        }
        price_info = json.dumps(price_info)
        producer.send(topic = 'prices', value = price_info.encode('utf-8'))
        producer.flush()
        time.sleep(1)

def consume():
    consumer.subscribe(topics=['orders'])
    for msg in consumer:
        req = json.loads(msg.value.decode('utf-8'))
        id = req.get('id')
        type = req.get('type')
        quantity = int(req.get('quantity'))
        price = float(req.get('price'))
        current_price = prices[current_index]
        if type == 'BUY':
            if price > current_price - eps:
                send_order_status(id, 'CONFIRMED', type, quantity, current_price + delta)
            else:
                send_order_status(id, 'CANCELLED', type, quantity, price)
        elif type == 'SELL':
            if price < current_price + eps:
                send_order_status(id, 'CONFIRMED', type, quantity, current_price - delta)
            else:
                send_order_status(id, 'CANCELLED', type, quantity, price)
        else:
            send_order_status(id, 'CANCELLED', type, quantity, price)
        time.sleep(0.001)

producer_thread = threading.Thread(target=produce)
consumer_thread = threading.Thread(target=consume)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print('exchange done')