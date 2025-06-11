from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from challenge._email.email_service import EmailService
from challenge.core.models import RevokedToken, User
from challenge.core.serializers import ChangePasswordSerializer, LoginSerializer, SignUpSerializer

from datetime import datetime, timedelta


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(user=user, data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Senha alterada com sucesso'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "Um email deve ser fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        token = AccessToken.for_user(user)
        token.set_exp(lifetime=timedelta(minutes=15))
        EmailService.send_reset_password_email(user, str(token), request)
        
        return Response({"message": "Email enviado"}, status=status.HTTP_200_OK)

    
class ResetPassword(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, token):
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')

        if new_password != new_password_confirm:
            return Response({"message": "As senhas não coincidem"}, status.HTTP_400_BAD_REQUEST)
    
        try:
            token_instance = AccessToken(token)
            user_id = token_instance['user_id']
            
            # Verificar se o token expirou
            if datetime.now() > datetime.fromtimestamp(token_instance['exp']):
                return Response({'message': 'O token expirou'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar se o token já foi usado
            if RevokedToken.objects.filter(user_id=user_id, token=token).exists():
                return Response({"message": "Token expirado"}, status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            
            # Definir a nova senha para o usuário
            user.set_password(new_password)
            user.save()
            
            # Revogar o token
            RevokedToken.objects.create(user=user, token=token)
            return Response({'message': 'Senha redefinida com sucesso'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': f"Erro ao redefinir a senha: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        