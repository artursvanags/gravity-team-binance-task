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
print(start_time, end_time)
# Convert start and end time to milliseconds
start_time = int(time.mktime(start_time.timetuple()))*1000
end_time = int(time.mktime(end_time.timetuple()))*1000

# Binance Kline Data API 
kline_api_endpoint = f"{url}/api/v3/klines?symbol={coin}&interval={candle_interval}"

# Fetch candle data and loop trough all the data to get all the candles and avoid 1000 API limit
def fetch_candle_data(start_time, end_time):
    data = []
    temp_end_time = end_time
    one_step = 60 * 1000 * 1000  # 1000 minutes in milliseconds
    
    while True:
        if end_time - start_time > one_step :
            temp_end_time = start_time + one_step
        try:
            response = requests.get(f"{kline_api_endpoint}&startTime={start_time}&endTime={temp_end_time}")
            data.extend(json.loads(response.text))
            if temp_end_time == end_time:
                break
            start_time = temp_end_time + 1
            if end_time - start_time > one_step :
                temp_end_time = start_time + one_step
            else:
                temp_end_time = end_time
        except Exception as e:
            print(f"An error occured while fetching data: {e}")
            break
    return pd.DataFrame(data)

df = fetch_candle_data(start_time, end_time)

try:
    df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 
                'close_time', 'quote_asset_volume', 'number_of_trades', 
                'taker_buy_base', 'taker_buy_quote', 'ignore']
    
    # Convert volume and close to numeric
    df[['volume', 'close']] = df[['volume', 'close']].astype(float)
    
    # Calculate VWAP
    total_usdt = (df['volume'] * df['close']).sum()
    total_eth = df['volume'].sum()
    vwap = total_usdt / total_eth
    vwap_decimal_part = str(vwap).split('.')[1][:8]
    sum_of_digits = sum(int(digit) for digit in vwap_decimal_part)

    print('Volume Weighted Average Price (VWAP) is: ', vwap)
    print('The sum of the first 8 digits after the decimal point is: ', sum_of_digits)

    # Export data to CSV file
    df.to_csv('Binance_ETHUSDT_data.csv',index=False)
    
except Exception as e:
    print(f"An error occured while fetching data: {e}")