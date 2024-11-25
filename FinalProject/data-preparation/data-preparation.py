# use yfinance to get price data, transform it into format we want, and save in the file
# do it for both exchange and for ML training
import os
import requests
from dotenv import load_dotenv, find_dotenv
from polygon import RESTClient

load_dotenv(find_dotenv())
POLYGON_API_KEY = os.getenv("polygon_api_key")

ticker = "AAPL"
client = RESTClient(api_key=POLYGON_API_KEY)

aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="second", from_="2024-11-01", to="2024-11-20", limit=50000):
    aggs.append(a)

print(aggs)
