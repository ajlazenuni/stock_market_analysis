import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from flask import Flask, jsonify
import matplotlib.pyplot as plt

app = Flask(__name__)

def calculate_indicators(data):
    data['RSI'] = RSIIndicator(data['last_trade_price'], window=14).rsi()

    data['SMA_50'] = SMAIndicator(data['last_trade_price'], window=50).sma_indicator()
    data['SMA_200'] = SMAIndicator(data['last_trade_price'], window=200).sma_indicator()

    data['EMA_50'] = EMAIndicator(data['last_trade_price'], window=50).ema_indicator()

    macd = MACD(data['last_trade_price'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()

    return data

def generate_signals(data):
    data['Signal'] = 'Hold'
    data.loc[data['SMA_50'] > data['SMA_200'], 'Signal'] = 'Buy'
    data.loc[data['SMA_50'] < data['SMA_200'], 'Signal'] = 'Sell'
    return data

@app.route('/api/analysis', methods=['GET'])
def analysis():
    data = pd.read_csv('/Users/ajlazenuni/PycharmProjects/stock_market_analysis/data/processed/all_symbols_20241110.csv', parse_dates=['date'])
    data.set_index('date', inplace=True)

    data = calculate_indicators(data)
    data = generate_signals(data)

    result = {
        str(date): row for date, row in data[['last_trade_price', 'RSI', 'SMA_50', 'SMA_200', 'Signal']].tail(10).iterrows()
    }
    return jsonify(result)

def visualize(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['last_trade_price'], label='Stock Price', color='blue')
    plt.plot(data.index, data['SMA_50'], label='SMA 50', linestyle='--', color='orange')
    plt.plot(data.index, data['SMA_200'], label='SMA 200', linestyle='--', color='red')

    buy_signals = data[data['Signal'] == 'Buy']
    sell_signals = data[data['Signal'] == 'Sell']
    plt.scatter(buy_signals.index, buy_signals['last_trade_price'], label='Buy Signal', marker='^', color='green', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['last_trade_price'], label='Sell Signal', marker='v', color='red', alpha=1)

    plt.title('Technical Analysis Visualization')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    data = pd.read_csv('/Users/ajlazenuni/PycharmProjects/stock_market_analysis/data/processed/all_symbols_20241110.csv', parse_dates=['date'])
    data.set_index('date', inplace=True)
    data = calculate_indicators(data)
    data = generate_signals(data)
    visualize(data)
    app.run(debug=True)
