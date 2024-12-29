from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from analysis.technical import TechnicalAnalysis

app = Flask(__name__)
CORS(app)

def load_data(symbol=None):
    data = pd.read_csv('all_symbols_20241110.csv', parse_dates=['date'])
    if symbol:
        data = data[data['symbol'] == symbol]
    data.sort_values('date', inplace=True)
    data.set_index('date', inplace=True)
    return data

@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    data = pd.read_csv('all_symbols_20241110.csv')
    symbols = data['symbol'].unique().tolist()
    return jsonify(symbols)

@app.route('/api/analysis/<symbol>', methods=['GET'])
def analysis(symbol):
    try:
        period = request.args.get('period', 'daily')
        print(f"Processing analysis for {symbol} with period {period}")  # Debug log
        
        # Load data for the specific symbol
        data = load_data(symbol)
        
        if data.empty:
            return jsonify({'error': f'No data found for symbol {symbol}'}), 404
        
        # Perform technical analysis
        tech_analysis = TechnicalAnalysis(data)
        result = tech_analysis.analyze()
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error processing analysis: {str(e)}")  # Error log
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<symbol>/all-periods', methods=['GET'])
def analysis_all_periods(symbol):
    try:
        # Load data for the specific symbol
        data = load_data(symbol)
        
        if data.empty:
            return jsonify({'error': f'No data found for symbol {symbol}'}), 404
        
        # Perform technical analysis for all time periods
        tech_analysis = TechnicalAnalysis(data)
        result = tech_analysis.analyze()
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in analysis_all_periods: {str(e)}")  # For debugging
        return jsonify({'error': str(e)}), 500

@app.route('/api/overview', methods=['GET'])
def market_overview():
    try:
        # Load the latest data for all symbols
        data = load_data()
        latest_date = data.index.max()
        latest_data = data[data.index == latest_date]
        
        overview = {
            'total_symbols': len(latest_data),
            'total_volume': float(latest_data['volume'].sum()),
            'total_turnover': float(latest_data['total_turnover'].sum()),
            'symbols_data': [{
                'symbol': row['symbol'],
                'last_price': float(row['last_trade_price']),
                'change_percentage': float(row['change_percentage']),
                'volume': float(row['volume'])
            } for _, row in latest_data.iterrows()]
        }
        
        return jsonify(overview)
    
    except Exception as e:
        print(f"Error in market_overview: {str(e)}")  # For debugging
        return jsonify({'error': str(e)}), 500

@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    """Return list of available technical indicators"""
    indicators = {
        'oscillators': [
            {'key': 'RSI', 'name': 'Relative Strength Index'},
            {'key': 'Stochastic', 'name': 'Stochastic Oscillator'},
            {'key': 'Williams_R', 'name': 'Williams %R'},
            {'key': 'MACD', 'name': 'Moving Average Convergence Divergence'},
            {'key': 'Daily_Return', 'name': 'Daily Return'}
        ],
        'moving_averages': [
            {'key': 'SMA_20', 'name': '20-day Simple Moving Average'},
            {'key': 'SMA_50', 'name': '50-day Simple Moving Average'},
            {'key': 'SMA_200', 'name': '200-day Simple Moving Average'},
            {'key': 'EMA_20', 'name': '20-day Exponential Moving Average'},
            {'key': 'EMA_50', 'name': '50-day Exponential Moving Average'}
        ],
        'time_periods': [
            {'key': 'daily', 'name': 'Daily'},
            {'key': 'weekly', 'name': 'Weekly'},
            {'key': 'monthly', 'name': 'Monthly'}
        ]
    }
    return jsonify(indicators)

if __name__ == '__main__':
    app.run(debug=True, port=5000)