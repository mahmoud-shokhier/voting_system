from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import  api_view, schema
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import CreateAPIView

from .models import *
from .logic.jwt_auth import JWT_Auth
from .serializers import *

class Login(CreateAPIView):
    serializer_class = LoginSerializers
    def create(self, request, *args, **kwargs):
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        auth = JWT_Auth()
        token = auth.generate_token(user, 'secret', 600)
        refresh_token = auth.generate_token(user, 'secret_refresh', 3600)
     
        Token.objects.update_or_create(
            user=user,
            defaults={'token': token, 'refresh_token': refresh_token},
        )
        return Response({
            'token':token, 
            'refresh_token':refresh_token, 
        })

class RefreshToken(CreateAPIView):
    serializer_class = RefreshTokenSerializer
    queryset = ''
    
    def create(self, request, *args, **kwargs):
        data=request.data
        serializer = RefreshTokenSerializer(data=request.data)
        auth = JWT_Auth()
        serializer.is_valid(raise_exception=True)
        print(data['refresh_token'])
        if auth.check_token(data['refresh_token'], 'secret_refresh'):
            user = serializer.validated_data['user']
            auth = JWT_Auth()
            token = auth.generate_token(user,'secret', 600)
            refresh_token = auth.generate_token(user,'secret_refresh', 3600)
            Token.objects.filter(user=user).update(token=token, refresh_token=refresh_token)
            return Response(
                {
                    'message':'token refreshed successfully',
                    'token': token, 
                    'refresh_token':refresh_token, 
                })
        else:
            msg = _('refresh token is expired.')
            raise serializers.ValidationError(msg, code='authorization')
