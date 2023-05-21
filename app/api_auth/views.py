from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
# Importamos el modelo de usuarios
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username,password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            context = {
                'status':True,
                'content':{
                    'username':user.username,
                    'fullname':user.first_name + ' ' + user.last_name,
                    'token':str(refresh.access_token),
                },
            }
        else:
            context = {
                'status':False,
                'content':'Credenciales no válidas',
            }
        
        return Response(context)