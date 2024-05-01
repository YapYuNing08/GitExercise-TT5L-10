from django.urls import path
from .views import  OrderDetails, Dashboard

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    
    # path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/', OrderDetails.as_view(), name='order_details'),
]