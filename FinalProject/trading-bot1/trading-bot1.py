import os 
import time
import json
import sys
import secrets
import string

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

producer = KafkaProducer(bootstrap_servers = 'kafka:9092',
                         acks = 0,
                         api_version = (0, 11, 5))

consumer1 = KafkaConsumer(bootstrap_servers = 'kafka:9092',
                         api_version = (0, 11, 5), consumer_timeout_ms = 15000)

consumer2 = KafkaConsumer(bootstrap_servers = 'kafka:9092',
                         api_version = (0, 11, 5), consumer_timeout_ms = 150000)

bot_id = 'bot1_'

time.sleep(1)

def generate_id():
    characters = string.ascii_letters + string.digits
    generated_id = ''.join(secrets.choice(characters) for _ in range(10))
    return bot_id + generated_id

# TODO Load a pre-trained model / models and make predictions
prices = []

def predict_next_price():
    return 0

opening_orders = set()
closing_orders = set()

delta = 0.009

def create_order(id, type, quantity, price):
    order = {
        'id': id,
        'type': type,
        'quantity': quantity,
        'price': price
    }
    return order

def send_order(order):
    order = json.dumps(order)
    producer.send(topic = 'orders', value = order.encode('utf-8'))
    producer.flush()

def other_type(type):
    if type == 'BUY':
        return 'SELL'
    elif type == 'SELL':
        return 'BUY'
    else:
        return ''

def consume_prices():
    consumer1.subscribe(topics=['prices'])
    for msg in consumer1:
        req = json.loads(msg.value.decode('utf-8'))
        price = float(req.get('price'))
        prices.append(price)
        next_price = predict_next_price()
        if next_price > price + delta:
            id = generate_id()
            order = create_order(id, 'BUY', 1, price)
            send_order(order)
            opening_orders.add(id)
        elif next_price < price - delta:
            id = generate_id()
            order = create_order(id, 'SELL', 1, price)
            send_order(order)
            opening_orders.add(id)
           
        time.sleep(0.001)

def consume_orders_status():
    consumer2.subscribe(topics=['orders_status'])
    for msg in consumer2:
        req = json.loads(msg.value.decode('utf-8'))
        id = req.get('id')
        if (not id) or (not id.startswith(bot_id)):
            continue

        status = req.get('status')
        type = req.get('type')
        quantity = int(req.get('quantity'))

        if status == 'CONFIRMED' and id in opening_orders:
            opening_orders.discard(id)
            new_id = generate_id()
            time.sleep(1)
            current_price = prices[-1]
            order = create_order(new_id, other_type(type), quantity, current_price)
            send_order(order)
            closing_orders.add(new_id)
        elif status == 'CANCELLED' and id in opening_orders:
            opening_orders.discard(id)
            time.sleep(0.001)
        elif status == 'CONFIRMED' and id in closing_orders:
            closing_orders.discard(id)
            time.sleep(0.001)
        elif status == 'CANCELLED' and id in closing_orders:
            closing_orders.discard(id)
            new_id = generate_id()
            time.sleep(1)
            current_price = prices[-1]
            order = create_order(new_id, type, quantity, current_price)
            send_order(order)
            closing_orders.add(new_id)

thread1 = threading.Thread(target=consume_prices)
thread2 = threading.Thread(target=consume_orders_status)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print('trading bot 1 done')
