from datetime import datetime, date

class DataValidator:
    @staticmethod
    def validate_data(data_rows):
        if not data_rows:
            print("No data to validate")
            return False

        valid_rows = []
        invalid_rows = []

        for row in data_rows:
            try:
                if len(row) != 10:
                    invalid_rows.append(row)
                    continue

                if not all([
                    isinstance(row[0], date),        # Date
                    isinstance(row[1], str),         # Symbol
                    all(isinstance(x, (float, int)) for x in row[2:])  # Numeric values
                ]):
                    invalid_rows.append(row)
                    continue

                valid_rows.append(row)

            except Exception as e:
                print(f"Error validating row: {row}, Error: {str(e)}")
                invalid_rows.append(row)

        print(f"Validated {len(valid_rows)} rows, Found {len(invalid_rows)} invalid rows")
        return valid_rows