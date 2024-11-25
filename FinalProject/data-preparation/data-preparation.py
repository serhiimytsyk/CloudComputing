import os
from dotenv import load_dotenv
import pandas as pd
from datetime import time
from polygon import RESTClient

load_dotenv()

POLYGON_API_KEY = os.getenv("polygon_api_key")

ticker = "AAPL"
client = RESTClient(api_key=POLYGON_API_KEY)

aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2024-11-01", to="2024-11-20", limit=50000):
    aggs.append(a)

df = pd.DataFrame(aggs)
df['price'] = df['vwap']
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time
df = df.drop(columns=['otc', 'transactions', 'open', 'high', 'low', 'close', 'volume', 'vwap'])
df = df[(df['time'] >= time(8, 0, 0)) & (df['time'] < time(18, 0, 0))]

date_to_prices = {}

date_to_prices = df.groupby('date')['price'].apply(list)
date_to_counts = date_to_prices.apply(len)
for date, count in date_to_counts.items():
    print(date, count)

for date, prices in date_to_prices.items():
    print(str(date), prices)
    with open('./' + str(date) + '.txt', 'w') as file:
        file.write(' '.join(map(str, prices)))
