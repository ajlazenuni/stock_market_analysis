import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import urllib.parse
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.connection = None
        self.connect()

    def connect(self):
        try:
            connection_url = os.getenv('MYSQL_HOST')
            parsed_url = urllib.parse.urlparse(connection_url)

            self.connection = mysql.connector.connect(
                host=parsed_url.hostname,
                port=int(os.getenv('MYSQL_PORT')),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE'),
                ssl_disabled=False
            )
            print("Successfully connected to Aiven MySQL database")
            self.create_tables()
        except Error as e:
            print(f"Error connecting to Aiven MySQL: {e}")

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    symbol VARCHAR(10) NOT NULL,
                    last_trade_price DECIMAL(10,2),
                    max_price DECIMAL(10,2),
                    min_price DECIMAL(10,2),
                    avg_price DECIMAL(10,2),
                    change_percentage DECIMAL(5,2),
                    volume INT,
                    turnover_best DECIMAL(15,2),
                    total_turnover DECIMAL(15,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_symbol_date (symbol, date)
                )
            """)
            self.connection.commit()
            print("Tables created successfully")
        except Error as e:
            print(f"Error creating tables: {e}")

    def batch_save_stock_data(self, data_rows, batch_size=1000):
        try:
            total_saved = 0
            for i in range(0, len(data_rows), batch_size):
                batch = data_rows[i:i + batch_size]
                cursor = self.connection.cursor()
                query = """
                    INSERT INTO stock_data (
                        date, symbol, last_trade_price, max_price,
                        min_price, avg_price, change_percentage,
                        volume, turnover_best, total_turnover
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.executemany(query, batch)
                self.connection.commit()
                total_saved += len(batch)
                print(f"Saved batch of {len(batch)} rows. Total saved: {total_saved}")

        except Error as e:
            print(f"Error in batch save: {e}")
            self.connection.rollback()

    def get_last_date(self, symbol):
        try:
            cursor = self.connection.cursor()
            query = "SELECT MAX(date) FROM stock_data WHERE symbol = %s"
            cursor.execute(query, (symbol,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else None
        except Error as e:
            print(f"Error getting last date for {symbol}: {e}")
            return None

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()