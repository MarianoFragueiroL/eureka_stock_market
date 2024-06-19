import requests
import os
from rest_framework import status,  generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..serializers import StockRequestSerializer

class StockInfoView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StockRequestSerializer

    def create(self, request, *args, **kwargs):
        api_key = os.environ.get('ALPHA_APIKEY', 'demo')
        base_url = os.environ.get('STOCK_URL', 'https://www.alphavantage.co/')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        symbol = serializer.validated_data.get('symbol')
        interval = serializer.validated_data.get('interval', 'daily')
        time_period = serializer.validated_data.get('time_period')
        series_type = serializer.validated_data.get('series_type', 'close')

        # Construir la URL de solicitud
        url = self.build_url(base_url, api_key, symbol, interval, time_period, series_type)

        # Realizar la solicitud a Alpha Vantage
        data = self.fetch_stock_data(url)

        if 'Error Message' in data:
            return Response({"error": data['Error Message']}, status=status.HTTP_400_BAD_REQUEST)
        if 'Note' in data:
            return Response({"error": "API call limit reached. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Calcular la variación entre los últimos dos valores de cierre
        variation = self.calculate_variation(data)

        # Añadir la variación a Meta Data
        if variation is not None:
            data['Meta Data']['last day variation'] = variation

        return Response(data, status=status.HTTP_200_OK)

    def build_url(self, base_url, api_key, symbol, interval, time_period, series_type):
        params = f'query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        url = f'{base_url}{params}'
        if interval:
            url += f'&interval={interval}'
        if time_period:
            url += f'&time_period={time_period}'
        if series_type:
            url += f'&series_type={series_type}'
        return url

    def fetch_stock_data(self, url):
        response = requests.get(url)
        return response.json()

    def calculate_variation(self, data):
        time_series = data.get("Time Series (Daily)", {})
        dates = sorted(time_series.keys(), reverse=True)
        if len(dates) < 2:
            return None

        latest_close = float(time_series[dates[0]]["4. close"])
        previous_close = float(time_series[dates[1]]["4. close"])
        return latest_close - previous_close