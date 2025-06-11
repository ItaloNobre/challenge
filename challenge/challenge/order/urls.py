from django.urls import path

from challenge.order.views import OrderViewSet, OrderLogHistoryView

urlpatterns = [
    # ORDER
    path('', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('<uuid:pk>/', OrderViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),

    path("history/", OrderLogHistoryView.as_view(), name="order-log"),

]
