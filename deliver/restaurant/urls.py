from django.urls import path
from .views import Dashboard, OrderDetails, Index, ReservationDetail

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order_details'),
    path('restaurant/index/', Index.as_view(), name='restaurant_index'),
    path('reservation_detail/', ReservationDetail.as_view(), name='reservation_detail'),
]