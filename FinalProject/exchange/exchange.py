import time
import json
import sys

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

import threading

print('0')

from kafka import KafkaProducer
from kafka import KafkaConsumer

print('1')

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         acks=0,
                         api_version=(0, 11, 5))

consumer = KafkaConsumer(bootstrap_servers='kafka:9092',
                         api_version=(0, 11, 5), consumer_timeout_ms = 600000)

print('2')

prices = []
with open('./2024-11-20.txt', 'r') as file:
    content = file.read()
    prices = list(map(float, content.split()))

delta = 0.001
eps = 0.00001
current_index = 0

print('3')

def send_order_status(id, status, type_, quantity, price):
    status = {
        'id': id,
        'status': status,
        'type': type_,
        'quantity': quantity,
        'price': price
    }
    status = json.dumps(status)
    producer.send(topic = 'orders_status', value = status.encode('utf-8'))
    print('Order', id, 'status is', status, 'for', type_, quantity, 'at', price, 'while current price is', prices[current_index])
    producer.flush()

time.sleep(10)

def produce():
    print('4')
    global current_index
    for i in range(len(prices)):
        price_info = {
            'price': prices[i]
        }
        price_info = json.dumps(price_info)
        producer.send(topic = 'prices', value = price_info.encode('utf-8'))
        producer.flush()
        current_index = i
        print('produce', current_index)
        print('Current price is', prices[i])
        time.sleep(1)

def consume():
    print('5')
    consumer.subscribe(topics=['orders'])
    for msg in consumer:
        print('consume', current_index)
        req = json.loads(msg.value.decode('utf-8'))
        id = req.get('id')
        type_ = req.get('type')
        quantity = int(req.get('quantity'))
        price = float(req.get('price'))
        current_price = prices[current_index]
        print('Received order', id, 'for', type_, quantity, 'at', price, 'while current price is', prices[current_index])
        if type_ == 'BUY':
            if price > current_price - eps:
                send_order_status(id, 'CONFIRMED', type_, quantity, current_price + delta)
            else:
                send_order_status(id, 'CANCELLED', type_, quantity, price)
        elif type_ == 'SELL':
            if price < current_price + eps:
                send_order_status(id, 'CONFIRMED', type_, quantity, current_price - delta)
            else:
                send_order_status(id, 'CANCELLED', type_, quantity, price)
        else:
            send_order_status(id, 'CANCELLED', type_, quantity, price)
        time.sleep(0.001)

producer_thread = threading.Thread(target=produce)
consumer_thread = threading.Thread(target=consume)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print('exchange done')