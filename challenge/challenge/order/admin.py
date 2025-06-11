
from django.contrib import admin
from .models import OrderStatus, Order


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ('code',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'status', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'code')
    list_filter = ('status', 'is_active')
    ordering = ('-created_at',)
