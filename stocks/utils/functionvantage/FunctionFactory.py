from .FunctionVantage import TimeSeriesIntraday, FunctionsVantage, TimeSeriesDaily, TimeSeriesDailyAdjusted, TimeSeriesWeekly,TimeSeriesWeeklyAdjusted, TimeSeriesMonthly, TimeSeriesMonthlyAdjusted

class FunctionsVantageFactory:
    _mapping = {
        'TIME_SERIES_INTRADAY': TimeSeriesIntraday,
        'TIME_SERIES_DAILY': TimeSeriesDaily,
        'TIME_SERIES_DAILY_ADJUSTED': TimeSeriesDailyAdjusted,
        'TIME_SERIES_WEEKLY': TimeSeriesWeekly,
        'TIME_SERIES_WEEKLY_ADJUSTED': TimeSeriesWeeklyAdjusted,
        'TIME_SERIES_MONTHLY': TimeSeriesMonthly,
        'TIME_SERIES_MONTHLY_ADJUSTED': TimeSeriesMonthlyAdjusted,
    }

    @staticmethod
    def register_function(name, cls):
        if not issubclass(cls, FunctionsVantage):
            raise ValueError(f"Class {cls.__name__} is not a subclass of FunctionsVantage")
        FunctionsVantageFactory._mapping[name] = cls

    @staticmethod
    def create(function_name, symbol, api_key, **kwargs):
        if function_name in FunctionsVantageFactory._mapping:
            return FunctionsVantageFactory._mapping[function_name](symbol=symbol, api_key=api_key, **kwargs)
        else:
            raise ValueError(f"Unknown function name: {function_name}")
