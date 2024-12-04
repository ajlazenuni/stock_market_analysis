from src.filters.scraper_filter import ScraperFilter
from src.filters.date_checker_filter import DateCheckerFilter
from src.filters.data_processor_filter import DataProcessorFilter
import time

def main():
    print("Starting stock market data collection...")
    start_time = time.time()

    try:
        scraper = ScraperFilter()
        date_checker = DateCheckerFilter()
        processor = DataProcessorFilter()

        print("\nGetting stock symbols...")
        symbols = scraper.process()
        print(f"Found {len(symbols)} symbols to process")

        total_records = 0
        for i, symbol in enumerate(symbols, 1):
            print(f"\nProcessing symbol {i}/{len(symbols)}: {symbol}")

            date_range = date_checker.process(symbol)

            if date_range:
                data = processor.process((symbol, date_range))
                if data:
                    total_records += len(data)

        processor.exporter.export_combined_csv()

        execution_time = time.time() - start_time
        print("\nExecution Summary:")
        print(f"Time taken: {execution_time:.2f} seconds")
        print(f"Total symbols processed: {len(symbols)}")
        print(f"Total records collected: {total_records}")

    except Exception as e:
        print(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()