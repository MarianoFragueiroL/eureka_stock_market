import requests
import abc
import requests
import os

from .FunctionValidator import FunctionValidator

class FunctionsVantage(abc.ABC):
    VALIDATOR = FunctionValidator()
    def __init__(self, symbol, api_key, datatype=None,*args, **kwargs):
        self.symbol = symbol
        self.api_key = api_key
        self.base_url = os.environ.get('STOCK_URL', 'https://www.alphavantage.co/')
        self.datatype= self.VALIDATOR.validate_datatype(datatype)

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

class InvalidIntervalError(Exception):
    pass
class InvalidParameterError(Exception):
    pass

class TimeSeriesIntraday(FunctionsVantage):
    def __init__(self, symbol, api_key, interval, adjusted=True, extended_hours=True, month=None, outputsize='compact', datatype='json', *args, **kwargs):
        super().__init__(symbol, api_key, datatype, *args, **kwargs)
        self.interval = self.VALIDATOR.validate_interval(interval)
        self.adjusted = adjusted
        self.extended_hours = extended_hours
        self.month = self.VALIDATOR.validate_month(month)
        self.outputsize = self.VALIDATOR.validate_outputsize(outputsize)
    
    def get_function_name(self):
        return 'TIME_SERIES_INTRADAY'

    def get_data(self):
        params = {
            'interval': self.interval,
            'adjusted': 'true' if self.adjusted else 'false',
            'extended_hours': 'true' if self.extended_hours else 'false',
            'outputsize': self.outputsize,
            'datatype': self.datatype
        }
        if self.month:
            params['month'] = self.month
        return self.fetch_data(**params)

class TimeSeriesDaily(FunctionsVantage):
    def __init__(self, symbol, api_key, outputsize=None, datatype=None,*args, **kwargs):
        super().__init__(symbol, api_key, datatype, *args, **kwargs)
        self.outputsize = self.VALIDATOR.validate_outputsize(outputsize)

    def get_function_name(self):
        return 'TIME_SERIES_DAILY'

    def get_data(self):
        return self.fetch_data()

class TimeSeriesDailyAdjusted(FunctionsVantage):
    def __init__(self, symbol, api_key, outputsize=None, datatype=None,*args, **kwargs):
        super().__init__(symbol, api_key, datatype, *args, **kwargs)
        self.outputsize = self.VALIDATOR.validate_outputsize(outputsize)
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