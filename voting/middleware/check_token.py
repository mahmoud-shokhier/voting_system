      
from django.contrib.auth.models import User
from rest_framework import authentication, serializers
from django.utils.translation import gettext_lazy as _
from users.logic.jwt_auth import JWT_Auth

from users.models import *
class CheckTokenMiddleware(authentication.BaseAuthentication):
    def authenticate(self, request):
        print('request')
        header_token = request.META.get('HTTP_AUTHORIZATION')
        try:
            token = Token.objects.get(token=header_token)
            user = CustomUser.objects.get(id=token.user_id)
            auth = JWT_Auth()
            if auth.check_token(header_token, 'secret'):
                print('authenticated')
                return (user, None)
            else:
                raise serializers.ValidationError(_('Your token is expired.'), code='authorization')
        except: 
            raise serializers.ValidationError(_('Your token is not valid.'), code='authorization')
