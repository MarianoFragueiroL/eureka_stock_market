import requests
import os
from rest_framework import status,  generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..serializers import StockRequestSerializer

@method_decorator(csrf_exempt, name='dispatch')
class StockInfoView(generics.CreateAPIView):
    # permission_classes = [AllowAny]
    serializer_class = StockRequestSerializer

    def create(self, request, *args, **kwargs):
        api_key = os.environ.get('ALPHA_APIKEY', 'demo')
        base_url = os.environ.get('STOCK_URL', 'https://www.alphavantage.co/')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        symbol = serializer.validated_data.get('symbol')
        function = serializer.validated_data.get('function', 'TIME_SERIES_DAILY_ADJUSTED')

        params = f'query?function={function}&symbol={symbol}&apikey={api_key}'
        url = f'{base_url}{params}'

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo'

        response = requests.get(url)
        data = response.json()
        data = self.manage_response(data)

        if 'Error Message' in data:
            return Response({"error": data['Error Message']}, status=status.HTTP_400_BAD_REQUEST)
        if 'Note' in data:
            return Response({"error": "API call limit reached. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        return Response(data, status=status.HTTP_200_OK)



    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def manage_response(self, data):
        time_series = data.get("Time Series (Daily)", {})
        dates = sorted(time_series.keys(), reverse=True)
        if len(dates) < 2:
            return Response({"error": "Not enough data points to calculate variation."}, status=status.HTTP_400_BAD_REQUEST)

        latest_close = float(time_series[dates[0]]["4. close"])
        previous_close = float(time_series[dates[1]]["4. close"])
        variation = latest_close - previous_close

        data['Meta Data']['last day variation'] = variation
        return data