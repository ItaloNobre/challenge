import time
import logging
from celery import shared_task
from .models import Order, OrderStatus

logger_celery = logging.getLogger('celery')


@shared_task
def process_order_task(order_id):
    time.sleep(5)
    try:
        order = Order.objects.get(id=order_id)
        status, _ = OrderStatus.objects.get_or_create(
            name="Processado",
            defaults={"code": 2}
        )
        order.status = status
        order.save(update_fields=["status"])
        logger_celery.info(f"Pedido {order_id} foi processado com sucesso.")
    except Order.DoesNotExist:
        logger_celery.error(f"Pedido com ID {order_id} não encontrado.")
    except Exception as e:
        logger_celery.error(f"Erro ao processar pedido {order_id}: {e}")
