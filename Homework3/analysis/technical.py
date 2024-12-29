import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator, IchimokuIndicator
from ta.volatility import BollingerBands
from ta.others import DailyReturnIndicator

class TechnicalAnalysis:
    def __init__(self, data):
        self.data = data
        # Convert columns for TA calculations
        self.data['Close'] = self.data['last_trade_price']
        self.data['High'] = self.data['max_price']
        self.data['Low'] = self.data['min_price']
        self.data['Open'] = self.data['last_trade_price']  # Using last_trade_price as Open

    def calculate_time_period_data(self):
        # Reset index to make date a column
        data_with_date = self.data.reset_index()
        
        # Daily data
        daily_data = data_with_date.copy()
        
        # Weekly data
        weekly_data = data_with_date.resample('W', on='date').agg({
            'Close': 'last',
            'High': 'max',
            'Low': 'min',
            'volume': 'sum'
        })
        
        # Monthly data
        monthly_data = data_with_date.resample('ME', on='date').agg({
            'Close': 'last',
            'High': 'max',
            'Low': 'min',
            'volume': 'sum'
        })
        
        # Set date as index again for consistency
        daily_data.set_index('date', inplace=True)
        
        return {
            'daily': daily_data,
            'weekly': weekly_data,
            'monthly': monthly_data
        }

    def calculate_indicators(self, data):
        """Calculate all technical indicators for a given timeframe data"""
        # Oscillators (5)
        # 1. RSI
        data['RSI'] = RSIIndicator(data['Close'], window=14).rsi()
        
        # 2. Stochastic
        stoch = StochasticOscillator(data['High'], data['Low'], data['Close'])
        data['Stochastic_K'] = stoch.stoch()
        data['Stochastic_D'] = stoch.stoch_signal()
        
        # 3. Williams %R
        data['Williams_R'] = WilliamsRIndicator(data['High'], data['Low'], data['Close']).williams_r()
        
        # 4. MACD
        macd = MACD(data['Close'])
        data['MACD'] = macd.macd()
        data['MACD_Signal'] = macd.macd_signal()
        
        # 5. Daily Return
        data['Daily_Return'] = DailyReturnIndicator(data['Close']).daily_return()
        
        # Moving Averages (5)
        # 1. SMA 20
        data['SMA_20'] = SMAIndicator(data['Close'], window=20).sma_indicator()
        # 2. SMA 50
        data['SMA_50'] = SMAIndicator(data['Close'], window=50).sma_indicator()
        # 3. SMA 200
        data['SMA_200'] = SMAIndicator(data['Close'], window=200).sma_indicator()
        # 4. EMA 20
        data['EMA_20'] = EMAIndicator(data['Close'], window=20).ema_indicator()
        # 5. EMA 50
        data['EMA_50'] = EMAIndicator(data['Close'], window=50).ema_indicator()
        
        # Additional Indicators
        bollinger = BollingerBands(data['Close'])
        data['BB_Upper'] = bollinger.bollinger_hband()
        data['BB_Lower'] = bollinger.bollinger_lband()
        
        return data

    def generate_signals(self, data):
        """Generate trading signals based on technical indicators"""
        data['Signal'] = 'Hold'
        
        # Moving Average Signals
        data.loc[data['SMA_50'] > data['SMA_200'], 'Signal'] = 'Buy'  # Golden Cross
        data.loc[data['SMA_50'] < data['SMA_200'], 'Signal'] = 'Sell'  # Death Cross
        
        # RSI Signals
        data.loc[data['RSI'] < 30, 'Signal'] = 'Buy'  # Oversold
        data.loc[data['RSI'] > 70, 'Signal'] = 'Sell'  # Overbought
        
        # MACD Signals
        data.loc[(data['MACD'] > data['MACD_Signal']), 'Signal'] = 'Buy'
        data.loc[(data['MACD'] < data['MACD_Signal']), 'Signal'] = 'Sell'
        
        # Stochastic Signals
        data.loc[(data['Stochastic_K'] < 20) & (data['Stochastic_D'] < 20), 'Signal'] = 'Buy'
        data.loc[(data['Stochastic_K'] > 80) & (data['Stochastic_D'] > 80), 'Signal'] = 'Sell'
        
        # Williams %R Signals
        data.loc[data['Williams_R'] < -80, 'Signal'] = 'Buy'
        data.loc[data['Williams_R'] > -20, 'Signal'] = 'Sell'
        
        return data

    def analyze(self):
        # Get data for different time periods
        timeframes = self.calculate_time_period_data()
        
        # Calculate indicators and signals for each timeframe
        analysis_results = {}
        for timeframe, data in timeframes.items():
            data_with_indicators = self.calculate_indicators(data)
            data_with_signals = self.generate_signals(data_with_indicators)
            
            # Get the latest values
            latest = data_with_signals.iloc[-1]
            
            analysis_results[timeframe] = {
                'symbol': latest.get('symbol', ''),
                'current_price': float(latest['Close']),
                'current_signal': latest['Signal'],
                'indicators': {
                    'RSI': float(latest['RSI']) if pd.notnull(latest['RSI']) else None,
                    'MACD': float(latest['MACD']) if pd.notnull(latest['MACD']) else None,
                    'MACD_Signal': float(latest['MACD_Signal']) if pd.notnull(latest['MACD_Signal']) else None,
                    'Stochastic_K': float(latest['Stochastic_K']) if pd.notnull(latest['Stochastic_K']) else None,
                    'Stochastic_D': float(latest['Stochastic_D']) if pd.notnull(latest['Stochastic_D']) else None,
                    'Williams_R': float(latest['Williams_R']) if pd.notnull(latest['Williams_R']) else None,
                    'SMA_20': float(latest['SMA_20']) if pd.notnull(latest['SMA_20']) else None,
                    'SMA_50': float(latest['SMA_50']) if pd.notnull(latest['SMA_50']) else None,
                    'SMA_200': float(latest['SMA_200']) if pd.notnull(latest['SMA_200']) else None,
                    'EMA_20': float(latest['EMA_20']) if pd.notnull(latest['EMA_20']) else None,
                    'EMA_50': float(latest['EMA_50']) if pd.notnull(latest['EMA_50']) else None,
                    'BB_Upper': float(latest['BB_Upper']) if pd.notnull(latest['BB_Upper']) else None,
                    'BB_Lower': float(latest['BB_Lower']) if pd.notnull(latest['BB_Lower']) else None,
                    'Daily_Return': float(latest['Daily_Return']) if pd.notnull(latest['Daily_Return']) else None
                },
                'historical_data': {
                    str(date): {
                        'price': float(row['Close']),
                        'volume': float(row['volume']),
                        'RSI': float(row['RSI']) if pd.notnull(row['RSI']) else None,
                        'Signal': row['Signal']
                    } for date, row in data_with_signals.tail(30).iterrows()
                }
            }
        
        return analysis_results