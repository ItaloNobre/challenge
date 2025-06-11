import uuid

from django.contrib.auth.models import User
from django.db import models

from challenge import settings
from challenge._utils.exeptions import CustomValidation


# Create your models here.


class OrderStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('nome', max_length=100, null=True, blank=True)
    code = models.IntegerField('codigo', null=True)

    is_active = models.BooleanField('ativo', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now=True)

    class Meta:
        db_table = 'order_status'
        verbose_name = "situação do Pedido"
        verbose_name_plural = "situação dos Pedidos"

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Titulo', max_length=50)
    code = models.IntegerField("Código do Pedido")
    status = models.ForeignKey(OrderStatus,verbose_name='Status', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Usuário', on_delete=models.PROTECT)
    description = models.TextField('Descrição', max_length=1000, null=True, blank=True)

    is_active = models.BooleanField('ativo', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_register = Order.objects.order_by('-code').first()
            if last_register is not None:
                self.code = last_register.code + 1
            else:
                self.code = 1
        if not self.status_id:
            default_status, _ = OrderStatus.objects.get_or_create(
                name="Pendente",
                defaults={"code": 1}
            )
            self.status = default_status
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'order'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'{self.title}'
