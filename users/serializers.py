from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import CustomUser, Token
from .logic.jwt_auth import JWT_Auth
class LoginSerializers(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password',]
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        username = data.get('email')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)
    
    def validate(self, data):
        refresh_token = data.get('refresh_token')
        token = Token.objects.filter(refresh_token=refresh_token)
        if len(token)>0:
            data['user']=CustomUser.objects.get(id=token[0].user_id)
            return data
        else:
            msg = _('Reresh token is not valid.')
            raise serializers.ValidationError(msg, code='authorization')

class RegisterSerializers(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password','name']
        write_only_fields = ('password',)
        read_only_fields = ('id',)
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )
    def create(self, validated_data):
        user = CustomUser.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user