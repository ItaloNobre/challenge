from rest_framework import serializers
from challenge._utils.exeptions import CustomSerializer, ValidateNameMixin
from challenge.order.models import Order, OrderStatus


class OrderStatusSerializer(CustomSerializer, ValidateNameMixin):

    class Meta:
        model = OrderStatus
        exclude = ['created_at', 'updated_at']


class OrderSerializer(CustomSerializer):

    class Meta:
        model = Order
        exclude = ['created_at', 'updated_at', 'user']
        read_only_fields = ['code', 'status']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['status'] = OrderStatusSerializer(instance.status).data
        return ret


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if request is None or request.user is None or request.user.is_anonymous:
            raise serializers.ValidationError({"message": "Usuário deve estar autenticado para criar um pedido."})

        order = Order.objects.create(user=user, **validated_data)
        return order


