from datetime import datetime


class DateCheckerFilter:
    def process(self, symbol):
        try:
            current_year = datetime.now().year
            start_year = current_year - 10

            return {
                'start_year': start_year,
                'end_year': current_year
            }
        except Exception as e:
            print(f"Error in date checker: {str(e)}")
            return None