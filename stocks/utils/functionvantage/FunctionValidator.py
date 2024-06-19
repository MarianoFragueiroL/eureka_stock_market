from datetime import datetime


class InvalidIntervalError(Exception):
    pass
class InvalidParameterError(Exception):
    pass

class FunctionValidator:
    VALID_INTERVALS = ['1min', '5min', '15min', '30min', '60min']
    VALID_OUTPUTSIZES = ['compact', 'full']
    VALID_DATATYPES = ['json', 'csv']
    def validate_interval(self, value):
        if value and value not in self.VALID_INTERVALS:
            raise InvalidParameterError(f"Invalid interval: {value}. Valid intervals are: {', '.join(self.VALID_INTERVALS)}")
        return value

    def validate_outputsize(self, value):
        if value and value not in self.VALID_OUTPUTSIZES:
            raise InvalidParameterError(f"Invalid outputsize: {value}. Valid outputsizes are: {', '.join(self.VALID_OUTPUTSIZES)}")
        return value

    def validate_datatype(self, value):
        if value and value not in self.VALID_DATATYPES:
            raise InvalidParameterError(f"Invalid datatype: {value}. Valid datatypes are: {', '.join(self.VALID_DATATYPES)}")
        return value

    def validate_month(self, value):
        if value:
            try:
                datetime.strptime(value, '%Y-%m')
            except ValueError:
                raise InvalidParameterError(f"Invalid month format: {value}. Expected format: YYYY-MM")
        return value