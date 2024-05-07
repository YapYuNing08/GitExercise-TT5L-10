from django.urls import path
from .views import Dashboard, OrderDetails, Index, ReservationDetails

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order_details'),
    path('restaurant/index/', Index.as_view(), name='restaurant_index'),
    path('restaurant/reservation_details/<int:pk>/', ReservationDetails.as_view(), name='reservation_details'),]