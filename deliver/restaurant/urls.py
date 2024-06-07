from django.urls import path
from .views import Dashboard, OrderDetails, Index, ReservationDetails, MarkAsServed
from . import views

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order_details'),
    path('restaurant/index/', Index.as_view(), name='restaurant_index'),
    path('restaurant/reservation_details/<int:pk>/', ReservationDetails.as_view(), name='reservation_details'),
    path('mark_as_served/<int:order_id>/', MarkAsServed.as_view(), name='mark_as_served'),
    path('restaurant/update_food_status/<int:order_id>/',views.update_food_status, name='update_food_status'),
    path('verify_claim/', views.verify_claim, name='verify_claim'),
    ]
