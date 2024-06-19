import requests
import os
from rest_framework import status,  generics
from rest_framework.response import Response
from rest_framework.response import Response
from ..serializers import StockRequestSerializer
from ..utils.functionvantage.FunctionFactory import FunctionsVantageFactory

class StockInfoView(generics.CreateAPIView):
    serializer_class = StockRequestSerializer

    def create(self, request, *args, **kwargs):
        api_key = os.environ.get('ALPHA_APIKEY', 'demo')
        base_url = os.environ.get('STOCK_URL', 'https://www.alphavantage.co/')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        symbol = serializer.validated_data.get('symbol')
        function = serializer.validated_data.get('function', 'TIME_SERIES_DAILY_ADJUSTED')
        interval = serializer.validated_data.get('interval', None)
        self.limit = serializer.validated_data.get('limit', 1)
        time_period = serializer.validated_data.get('time_period', None)
        series_type = serializer.validated_data.get('series_type', None)
        adjusted = serializer.validated_data.get('adjusted', True)
        extended_hours = serializer.validated_data.get('extended_hours', True)
        month = serializer.validated_data.get('month', None)
        outputsize = serializer.validated_data.get('outputsize', 'compact')
        datatype = serializer.validated_data.get('datatype', 'json')

        try:
            stock_instance = FunctionsVantageFactory.create(
                function,
                symbol,
                api_key,
                interval=interval,
                adjusted=adjusted,
                extended_hours=extended_hours,
                month=month,
                outputsize=outputsize,
                datatype=datatype
            )
            data = stock_instance.get_data()
            data = self.calculate_variation(data)
            
            if 'Error Message' in data:
                return Response({"error": data['Error Message']}, status=status.HTTP_400_BAD_REQUEST)
            if 'Note' in data:
                return Response({"error": "API call limit reached. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return self.handle_exception(e)

    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def calculate_variation(self, data):
        time_series_key = self._find_time_series_key(data)
        if time_series_key:
            time_series_data = data.get(time_series_key, {})
        if not time_series_data:
            return data["Meta Data"]
        dates = sorted(time_series_data.keys(), reverse=True)
        if len(dates) < 2:
            return data

        latest_close = float(time_series_data[dates[0]]["4. close"])
        previous_close = float(time_series_data[dates[1]]["4. close"])
        variation = latest_close - previous_close

        data["Meta Data"]['Variation'] = variation
        filtered_data = {
                "Meta Data": data.get("Meta Data", {}),
                f"Time Series {dates[0]}": [time_series_data[dates[i]] for i in range(self.limit) ]
            }
        return filtered_data
        
    def _find_time_series_key(self, data):
        for key in data.keys():
            if "Time Series" in key:
                return key
        return None