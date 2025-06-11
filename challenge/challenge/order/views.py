
import logging
from challenge.order.tasks import process_order_task

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets, status

from challenge._utils.pagination import Pagination
from challenge.order.filters import OrderFilter
from challenge.order.models import Order
from challenge.order.serializers import OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import os

logger = logging.getLogger('orders')


class OrderViewSet(viewsets.ModelViewSet):

    pagination_class = Pagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    def perform_destroy(self, instance):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=['is_active'])

        logger.info(
            f"Order {instance.id} marked as inactive by user {self.request.user.id} ({self.request.user.email})"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        order = serializer.save()
        process_order_task.delay(str(order.id))


class OrderLogHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        log_path = os.path.join('logs', 'celery.log')

        if not os.path.exists(log_path):
            return Response({"message": "Arquivo de log não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        logs = []
        with open(log_path, 'r', encoding='utf-8') as file:
            for line in file:
                if "Pedido" in line:
                    logs.append(line.strip())

        return Response(logs)
