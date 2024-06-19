from rest_framework import  status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from rest_framework.views import exception_handler

from ..serializers import UserSerializer

class SignUpView(generics.CreateAPIView):
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
                return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            user_data = UserSerializer(user).data
            api_key, key = APIKey.objects.create_key(name=user.username)
            return Response({"api_key": key, 'user_details': user_data}, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error": f'An error ocurred try later. Check: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
