from rest_framework import  status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from ..serializers import UserSerializer
from ..models import ApiKey


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not all([username, password]):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if user is not None:
                    # User exists and credentials are correct, return the API key
                    api_key, created = ApiKey.objects.get_or_create(user=user)
                    return Response({"api_key": api_key.key}, status=status.HTTP_200_OK)
                return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
            # Check if the user already exists
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": 'An error ocurred try later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
