from rest_framework import  status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from ..serializers import UserSerializer
from ..models import ApiKey


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')

        if not all([username, password]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            # User exists and credentials are correct, return the API key
            api_key = ApiKey.objects.get(user=user)
            return Response({"api_key": api_key.key}, status=status.HTTP_200_OK)
        else:
            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return Response({"error": "User exists but credentials are incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user and API key
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = User.objects.get(username=username)
            api_key = ApiKey.objects.get(user=user)
            headers = self.get_success_headers(serializer.data)
            return Response({"api_key": api_key.key}, status=status.HTTP_201_CREATED, headers=headers)
