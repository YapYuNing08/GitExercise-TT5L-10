from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel, ReservationModel
# from django.contrib.auth.decorators import login_required

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'restaurant/index.html')

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        # loop through the orders and add the price value
        total_revenue = sum(order.price for order in orders)

        total_orders = len(orders)
        
        # for order in orders:
        #     total_revenue += order.price

        # pass total number of orders and total revenue into template
        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': total_orders
        }

        return render(request, 'restaurant/dashboard.html', context)
    
class ReservationDetail(View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        reservations = ReservationModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        total_reservations = len(reservations)
    
        context = {
            'reservations': reservations,
            'total_reservation': total_reservations
        }

        return render(request, 'restaurant/reservation_detail.html', context)

class OrderDetails(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }

        return render(request, 'restaurant/order_details.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_served = True
        order.save()

        context = {
            'order':order
        }

        return render(request, 'restaurant/order_details.html', context)
    
class ReservationDetails(View):
    def get(self, request, pk, *args, **kwargs):
        reservation = ReservationModel.objects.get(pk=pk)
        reservations = ReservationModel.objects.all()
        context = {
            'reservation': reservation,
            'reservations': reservations
        }

        return render(request, 'restaurant/reservation_details.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        reservation = ReservationModel.objects.get(pk=pk)

        context = {
            'reservation':reservation
        }

        return render(request, 'restaurant/reservation_details.html', context)