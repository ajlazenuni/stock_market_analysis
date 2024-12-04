
import pandas as pd
from datetime import datetime
import os


class DataExporter:
    def __init__(self):
        self.base_dir = 'data/processed'
        os.makedirs(self.base_dir, exist_ok=True)
        self.all_data = []

    def add_data(self, data, symbol):
        self.all_data.extend(data)

    def export_combined_csv(self):
        try:
            if not self.all_data:
                print("No data to export")
                return None

            filename = f"{self.base_dir}/all_symbols_{datetime.now().strftime('%Y%m%d')}.csv"

            df = pd.DataFrame(self.all_data, columns=[
                'date', 'symbol', 'last_trade_price', 'max_price',
                'min_price', 'avg_price', 'change_percentage',
                'volume', 'turnover_best', 'total_turnover'
            ])

            df = df.sort_values(['symbol', 'date'])

            df.to_csv(filename, index=False)
            print(f"All data exported to {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting combined data to CSV: {e}")
            return None