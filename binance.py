import time
import datetime
import pandas as pd
import requests
import json
import pytz

# API endpoint
url = "https://api1.binance.com"

# Coin and interval
coin = "ETHUSDT"
candle_interval = "1m"  # 1 minute 

# Start and end time
start_time = datetime.datetime(2023, 1, 1, tzinfo=pytz.UTC)
end_time = datetime.datetime(2023, 1, 2, tzinfo=pytz.UTC)

# Convert start and end time to milliseconds
start_time = int(time.mktime(start_time.timetuple()))*1000
end_time = int(time.mktime(end_time.timetuple()))*1000

# Binance Kline Data API 
# https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
kline_api_endpoint = f"{url}/api/v3/klines?symbol={coin}&interval={candle_interval}&startTime={start_time}&endTime={end_time}"

try:
    response = requests.get(kline_api_endpoint)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 
                  'close_time', 'quote_asset_volume', 'number_of_trades', 
                  'taker_buy_base', 'taker_buy_quote', 'ignore']

    # Convert volume and close to numeric
    df[['volume', 'close']] = df[['volume', 'close']].astype(float)

    # Calculate VWAP
    round_to = 8
    total_usdt = (df['volume'] * df['close']).sum()
    total_eth = df['volume'].sum()
    vwap = round(total_usdt / total_eth, round_to)
    
    vwap_decimal_part = str(vwap).split('.')[1][:round_to]
    sum_of_digits = sum(int(digit) for digit in vwap_decimal_part)
    
    print('Volume Weighted Average Price (VWAP) is: ', vwap)
    print('The sum of the first 8 digits after the decimal point is: ', sum_of_digits)
    print( vwap_decimal_part)
    
except Exception as e:
    print(f"An error occured while fetching data: {e}")