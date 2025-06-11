from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import status
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from challenge.core.models import User
from challenge._utils.exeptions import CustomSerializer, CustomValidation


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserSerializer(CustomSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'email', 'full_name',]


class SignUpSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=250)
    password = serializers.CharField(write_only=True)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise CustomValidation("Um usuário com este e-mail já existe.", status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(value)
            return value
        except ValidationError:
            raise CustomValidation("Informe um endereço de email válido.", status.HTTP_400_BAD_REQUEST)


    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        tokens = get_tokens_for_user(instance)
        return {**UserSerializer(instance).data, **tokens}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate_email(self, value):
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise CustomValidation("Informe um endereço de email válido.", status.HTTP_400_BAD_REQUEST)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise CustomValidation("Credenciais inválidas ou usuário inexistente", status.HTTP_400_BAD_REQUEST)
        return user

    def to_representation(self, instance):
        tokens = get_tokens_for_user(instance)
        return {**UserSerializer(instance).data, **tokens}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[])
    confirm_new_password = serializers.CharField(required=True)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            raise CustomValidation("Senha antiga incorreta", status.HTTP_400_BAD_REQUEST)
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise CustomValidation("Nova senha e confirmação não correspondem.", status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            error_messages = [str(message) for message in e.messages]
            raise CustomValidation(error_messages[0], status.HTTP_400_BAD_REQUEST)

        return data
