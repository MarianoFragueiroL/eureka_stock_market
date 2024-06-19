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

        
        # Construir la URL de solicitud
        params = f'query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        url = f'{base_url}{params}'
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo'

        # if time_period:
        #     url += f'&time_period={time_period}'
        # if series_type:
        #     url += f'&series_type={series_type}'

        # Realizar la solicitud a Alpha Vantage
        response = requests.get(url)
        data = response.json()

        if 'Error Message' in data:
            return Response({"error": data['Error Message']}, status=status.HTTP_400_BAD_REQUEST)
        if 'Note' in data:
            return Response({"error": "API call limit reached. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        return Response(data, status=status.HTTP_200_OK)



    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

