import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from src.database.db_manager import DatabaseManager
from src.utils.data_validator import DataValidator
from src.utils.data_exporter import DataExporter


class DataProcessorFilter:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://www.mse.mk/en/stats/symbolhistory/"
        self.db = DatabaseManager()
        self.validator = DataValidator()
        self.exporter = DataExporter()

    def process(self, data):
        symbol, date_range = data
        if not date_range:
            return None

        try:
            print(f"Processing symbol: {symbol}")
            all_data = []

            for year in range(date_range['start_year'], date_range['end_year'] + 1):
                from_date = f'{year}-01-01'
                to_date = f'{year}-12-31'

                print(f"Fetching {symbol} data for year {year}")

                url = f"{self.base_url}{symbol}"
                params = {
                    'fromDate': from_date,
                    'toDate': to_date
                }

                response = requests.get(url, params=params)
                soup = BeautifulSoup(response.content, 'html.parser')

                table = soup.find('table')
                if not table:
                    continue

                rows = []
                for row in table.find_all('tr'):
                    columns = row.find_all(['th', 'td'])
                    rows.append([col.get_text(strip=True) for col in columns])

                if len(rows) > 1:
                    df = pd.DataFrame(rows[1:], columns=rows[0])  # Skip header row
                    all_data.extend(self.convert_to_db_format(df, symbol))

            valid_data = self.validator.validate_data(all_data)

            if valid_data:
                self.db.batch_save_stock_data(valid_data)

                self.exporter.add_data(valid_data, symbol)

                return valid_data

        except Exception as e:
            print(f"Error processing data for {symbol}: {str(e)}")
            return None

    def convert_to_db_format(self, df, symbol):
        """Convert pandas DataFrame to database format"""
        db_rows = []
        for _, row in df.iterrows():
            try:

                date = datetime.strptime(row['Date'], '%m/%d/%Y').date()


                db_row = (
                    date,
                    symbol,
                    self.parse_number(row.get('Last trade price', '0')),
                    self.parse_number(row.get('Max', '0')),
                    self.parse_number(row.get('Min', '0')),
                    self.parse_number(row.get('Avg. Price', '0')),
                    self.parse_number(row.get('%chg.', '0')),
                    int(self.parse_number(row.get('Volume', '0'))),
                    self.parse_number(row.get('Turnover in BEST in denars', '0')),
                    self.parse_number(row.get('Total turnover in denars', '0'))
                )
                db_rows.append(db_row)

            except Exception as e:
                print(f"Error processing row for {symbol}: {str(e)}")
                continue

        return db_rows

    @staticmethod
    def parse_number(value):

        try:

            clean_value = str(value).strip().replace(',', '').replace('%', '')
            return float(clean_value) if clean_value else 0.0
        except (ValueError, AttributeError):
            return 0.0

    @staticmethod
    def clean_symbol(symbol):

        return symbol.strip().upper()

    def validate_response(self, response):

        if response.status_code != 200:
            raise Exception(f"HTTP error {response.status_code}: {response.text}")
        return True

    def extract_table_data(self, soup):

        table = soup.find('table')
        if not table:
            return []

        rows = []
        for row in table.find_all('tr'):
            columns = row.find_all(['th', 'td'])
            if columns:
                rows.append([col.get_text(strip=True) for col in columns])

        return rows if len(rows) > 1 else []

    def create_dataframe(self, rows):

        if not rows:
            return None

        try:

            df = pd.DataFrame(rows[1:], columns=rows[0])
            return df
        except Exception as e:
            print(f"Error creating DataFrame: {str(e)}")
            return None