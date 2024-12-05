import time
import json
import sys

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves
    
import secrets
import string
import threading
from kafka import KafkaProducer
from kafka import KafkaConsumer

producer = KafkaProducer(bootstrap_servers = 'kafka:9092',
                         acks = 0,
                         api_version = (0, 11, 5))

consumer1 = KafkaConsumer(bootstrap_servers = 'kafka:9092',
                         api_version = (0, 11, 5), consumer_timeout_ms = 600000)

consumer2 = KafkaConsumer(bootstrap_servers = 'kafka:9092',
                         api_version = (0, 11, 5), consumer_timeout_ms = 600000)

bot_id = 'bot2_'

time.sleep(5)

def generate_id():
    characters = string.ascii_letters + string.digits
    generated_id = ''.join(secrets.choice(characters) for _ in range(10))
    return bot_id + generated_id

p, d, q = 2, 1, 1

l = 50

values = []

def predict_next_price(next_value, index):
    if len(values) == 0:
        values.append(next_value)
        return next_value
    else:
        values[-1] = values[-1] * 0.4 + 0.6 * next_value
        return values[-1]

opening_orders = set()
closing_orders = set()

delta = 0.01

def create_order(id, type_, quantity, price):
    order = {
        'id': id,
        'type': type_,
        'quantity': quantity,
        'price': price
    }
    print('We want to', type_, quantity, 'of stock at', price)
    return order

def send_order(order):
    order = json.dumps(order)
    producer.send(topic = 'orders', value = order.encode('utf-8'))
    producer.flush()

def other_type(type_):
    if type_ == 'BUY':
        return 'SELL'
    elif type_ == 'SELL':
        return 'BUY'
    else:
        return ''

def consume_prices():
    consumer1.subscribe(topics=['prices'])
    idx = 0
    for msg in consumer1:
        req = json.loads(msg.value.decode('utf-8'))
        price = float(req.get('price'))
        next_price = predict_next_price(price, idx)
        idx += 1
        print('Current price is', price, 'predicted next price is', next_price)
        if next_price == None:
            continue

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
        print(req)
        id = req.get('id')
        if (not id) or (not id.startswith(bot_id)):
            continue

        status = req.get('status')
        type_ = req.get('type')
        quantity = int(req.get('quantity'))

        if status == 'CONFIRMED' and id in opening_orders:
            opening_orders.discard(id)
            new_id = generate_id()
            time.sleep(1)
            current_price = values[-1]
            order = create_order(new_id, other_type(type_), quantity, current_price)
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
            current_price = values[-1]
            order = create_order(new_id, type_, quantity, current_price)
            send_order(order)
            closing_orders.add(new_id)

thread1 = threading.Thread(target=consume_prices)
thread2 = threading.Thread(target=consume_orders_status)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print('trading bot 2 done')
