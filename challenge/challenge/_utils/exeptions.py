from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomSerializer(serializers.ModelSerializer):
    """
    Classe base para serializers personalizados do Django REST Framework.

    Esta classe personaliza o comportamento padrão de validação dos serializers.
    Ela captura exceções de validação e formata a estrutura da mensagem de erro,
    retornando apenas o primeiro erro encontrado em um formato específico.

    Isso permite padronizar a estrutura de resposta de erros em todos os serializers
    que herdam dessa classe.
    """

    def to_internal_value(self, data):
        """
        Sobrescreve o método to_internal_value para capturar exceções de validação.
        """
        try:
            # Tenta validar os dados chamando o método to_internal_value do superclasse
            return super().to_internal_value(data)
        except ValidationError as exc:
            # Se uma ValidationError for capturada
            # Extrai o primeiro campo e o primeiro erro
            field, error_list = next(iter(exc.detail.items()))
            # Obtém a mensagem de erro como uma string
            error_message = str(error_list[0])
            if error_message == 'Este campo é obrigatório.':
                error_message = f"O campo {field} é obrigatório"
            # Levanta uma ValidationError com a mensagem customizada
            message = f"{error_message} - {field}"
            raise ValidationError({'message': message})

class CustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Um erro de validação ocorreu.'
    default_code = 'error'

    def __init__(self, detail, status_code=status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {'message': (_(detail))}

class ValidateNameMixin:
    def validate_name(self, value):
        model_class = self.Meta.model
        if model_class.objects.filter(name__iexact=value, is_active=True).exists():
            raise CustomValidation(f"Já existe um(a) {model_class._meta.verbose_name} com este nome.",
                                   status.HTTP_400_BAD_REQUEST)
        return value
