import requests
import abc
import requests
import os

class FunctionsVantage(abc.ABC):
    def __init__(self, symbol, api_key, *args, **kwargs):
        self.symbol = symbol
        self.api_key = api_key
        self.base_url = os.environ.get('STOCK_URL', 'https://www.alphavantage.co/')

    @abc.abstractmethod
    def get_function_name(self):
        pass

    def build_url(self, **params):
        url = f"{self.base_url}query?function={self.get_function_name()}&symbol={self.symbol}&apikey={self.api_key}"
        for key, value in params.items():
            url += f"&{key}={value}"
        print(url)
        return url

    def fetch_data(self, **params):
        url = self.build_url(**params)
        response = requests.get(url)
        return response.json()


class TimeSeriesIntraday(FunctionsVantage):
    VALID_INTERVALS = ['1min', '5min', '15min', '30min', '60min']

    def __init__(self, symbol, interval, api_key, *args, **kwargs):
        if interval not in self.VALID_INTERVALS:
            raise InvalidIntervalError(f"Invalid interval: {interval}. Valid intervals are: {', '.join(self.VALID_INTERVALS)}")
        super().__init__(symbol, api_key)
        self.interval = interval

    def get_function_name(self):
        return 'TIME_SERIES_INTRADAY'

    def get_data(self):
        return self.fetch_data(interval=self.interval)

class TimeSeriesDaily(FunctionsVantage):
    VALID_INTERVALS = ['1min', '5min', '15min', '30min', '60min']
    def __init__(self, symbol, interval, api_key, *args, **kwargs):
        if interval not in self.VALID_INTERVALS:
            raise InvalidIntervalError(f"Invalid interval: {interval}. Valid intervals are: {', '.join(self.VALID_INTERVALS)}")
        super().__init__(symbol, api_key)
        self.interval = interval
    def get_function_name(self):
        return 'TIME_SERIES_DAILY'

    def get_data(self):
        return self.fetch_data(interval=self.interval)

class TimeSeriesDailyAdjusted(FunctionsVantage):
    def get_function_name(self):
        return 'TIME_SERIES_DAILY_ADJUSTED'

    def get_data(self):
        return self.fetch_data()

class TimeSeriesWeekly(FunctionsVantage):
    def get_function_name(self):
        return 'TIME_SERIES_WEEKLY'

    def get_data(self):
        return self.fetch_data()

class TimeSeriesWeeklyAdjusted(FunctionsVantage):
    def get_function_name(self):
        return 'TIME_SERIES_WEEKLY_ADJUSTED'

    def get_data(self):
        return self.fetch_data()

class TimeSeriesMonthly(FunctionsVantage):
    def get_function_name(self):
        return 'TIME_SERIES_MONTHLY'

    def get_data(self):
        return self.fetch_data()

class TimeSeriesMonthlyAdjusted(FunctionsVantage):
    def get_function_name(self):
        return 'TIME_SERIES_MONTHLY_ADJUSTED'

    def get_data(self):
        return self.fetch_data()
class InvalidIntervalError(Exception):
    pass