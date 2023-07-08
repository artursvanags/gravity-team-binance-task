#### Volume Weighted Average Price Calculator for Binance trading data

This script will calculate the Volume Weighted Average Price (VWAP) for any given day based on 1 minute intervals of the trading data. It fetches the OHLC (Open, High, Low, Close) trading data from the Binance's API endpoint for the provided symbol and interval.

#### Requirements
* Python 3+
* Python libraries: pandas, requests, json, time, datetime & pytz

#### Execution

When executed, the provided Python script:

1. Structures the parameters for the API Call:
    - `url`: The base URL for the Binance's API endpoint.
    - `coin`: The asset pair to consider, in this case `ETH/USDT`.
    - `candle_interval`: The interval of the candles on which to perform trades calculation, set to `1m` which denotes 1 minute.
    - `start_time` and `end_time`: Set to January 1st, 2023 using datetime objects explicitly in UTC timezone.

2. Calls Binance's API endpoint `/api/v3/klines` and retrieves the OHLCV trading data at 1 minute resolution.

3. Retrives and processes the API response:
    - Decodes the JSON response and converts it into a pandas DataFrame.
    - Assign column names to the DataFrame for better readability.
    - Convert `volume` and `close` columns to float type.

4. Performs VWAP calculation:
    - VWAP calculation involves computing the product of the closing price and volume (amount of ETH traded), summed for all trades and divided by the total volume for the day.
    - The VWAP value is then rounded to 8 decimal places as per Binance's precision level for cryptocurrencies.

5. Extracts the first 8 digits after the decimal point and sums them.

6. Prints out the VWAP value and the sum of the first 8 digits after the decimal point.

#### Error Handling

In case of any exceptions such as an error in fetching data, the script prints out an error message describing the cause of the exception. Exception handling is done for the entire process to catch and report any unexpected error during execution.
