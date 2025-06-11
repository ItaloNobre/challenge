from django.urls import path

from challenge.order.views import OrderViewSet, OrderLogHistoryView

urlpatterns = [
    # ORDER
    path('', OrderViewSet.as_view({'get': 'list'})),
    path('create/', OrderViewSet.as_view({'post': 'create'})),
    path('<uuid:pk>/', OrderViewSet.as_view({'get': 'retrieve'})),
    path('update/<uuid:pk>/', OrderViewSet.as_view({'patch': 'partial_update'})),
    path('delete/<uuid:pk>/', OrderViewSet.as_view({'delete': 'destroy'})),

    path("api/v1/order/history/", OrderLogHistoryView.as_view(), name="order-log"),

]
