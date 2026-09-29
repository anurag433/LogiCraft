from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer,UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data = request.data) 
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({
                "message": "Registration successful.",
                "user": user_data
            },
            status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {
                    "message": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            username=username,
            password=password
        )
        if user is None:
            return Response(
                {
                    "message": "Invalid username or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
                
            },
            status=status.HTTP_200_OK
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "success": True,
            "data": serializer.data
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({
            "success": True,
            "message": "Logout successful."
        })
