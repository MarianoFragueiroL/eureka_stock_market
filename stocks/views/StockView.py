import requests
import os
from rest_framework import status,  generics
from rest_framework.response import Response
from rest_framework.response import Response
from ..serializers import StockRequestSerializer

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
        time_period = serializer.validated_data.get('time_period', None)
        series_type = serializer.validated_data.get('series_type', None)

        params = f'query?function={function}&symbol={symbol}&apikey={api_key}'
        url = f'{base_url}{params}'

        self.build_url(base_url, api_key, symbol, interval, time_period, series_type)
        data = self.fetch_stock_data(url)
        data = self.calculate_variation(data)

        if 'Error Message' in data:
            return Response({"error": data['Error Message']}, status=status.HTTP_400_BAD_REQUEST)
        if 'Note' in data:
            return Response({"error": "API call limit reached. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        return Response(data, status=status.HTTP_200_OK)

    def fetch_stock_data(self, url):
        response = requests.get(url)
        return response.json()
    def build_url(self, base_url, api_key, symbol, interval, time_period, series_type):
        params = f'query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        if interval:
            url += f'&interval={interval}'
        if time_period:
            url += f'&time_period={time_period}'
        if series_type:
            url += f'&series_type={series_type}'
        url = f'{base_url}{params}'
        return url

    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def calculate_variation(self, data):
        time_series = data.get("Time Series (Daily)", {})
        dates = sorted(time_series.keys(), reverse=True)
        if len(dates) < 2:
            return Response({"error": "Not enough data points to calculate variation."}, status=status.HTTP_400_BAD_REQUEST)

        latest_close = float(time_series[dates[0]]["4. close"])
        previous_close = float(time_series[dates[1]]["4. close"])
        variation = latest_close - previous_close

        data['Variation'] = variation
        return data