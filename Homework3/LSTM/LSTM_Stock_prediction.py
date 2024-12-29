import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split


class LSTMStockPrediction:
    def __init__(self, data_file, look_back=60, epochs=10):
        self.data_file = data_file
        self.look_back = look_back
        self.epochs = epochs

        self.df = self.load_data()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = self.scaler.fit_transform(self.df[['last_trade_price']].values)  # Use last_trade_price

        self.X, self.y = self.prepare_data()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2,
                                                                                shuffle=False)

        self.model = self.build_model()

    def load_data(self):
        df = pd.read_csv(self.data_file)
        df['Date'] = pd.to_datetime(df['date'])  # Ensure correct date format
        df.set_index('Date', inplace=True)
        return df

    def prepare_data(self):
        X, y = [], []
        for i in range(self.look_back, len(self.scaled_data)):
            X.append(self.scaled_data[i - self.look_back:i, 0])
            y.append(self.scaled_data[i, 0])
        X, y = np.array(X), np.array(y)

        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        return X, y

    def build_model(self):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(self.X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))  # Output layer for regression
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train_model(self):
        self.model.fit(self.X_train, self.y_train, epochs=self.epochs, batch_size=32)

    def predict(self):
        predictions = self.model.predict(self.X_test)
        predictions = self.scaler.inverse_transform(predictions)
        return predictions

    def plot_results(self, predictions):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df.index[-len(self.y_test):], self.scaler.inverse_transform(self.y_test.reshape(-1, 1)),
                 color='blue', label='True Price')
        plt.plot(self.df.index[-len(self.y_test):], predictions, color='red', label='Predicted Price')
        plt.title('Stock Price Prediction with LSTM')
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    lstm_model = LSTMStockPrediction(data_file='/Users/ajlazenuni/PycharmProjects/stock_market_analysis/data/processed/all_symbols_20241110.csv', look_back=60, epochs=10)
    lstm_model.train_model()
    predictions = lstm_model.predict()
    lstm_model.plot_results(predictions)
