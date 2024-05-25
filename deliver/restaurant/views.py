from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel, ReservationModel, OrderPlaced, Product
from django.http import JsonResponse, HttpResponse
import json
# from django.contrib.auth.decorators import login_required

class Index(View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderPlaced.objects.filter(
            ordered_date__year=today.year, ordered_date__month=today.month, ordered_date__day=today.day).order_by('-ordered_date')
        
        # loop through the orders and add the price value
        # total_revenue = sum(order.price for order in orders)

        total_orders = len(orders)
        
        # for order in orders:
        #     total_revenue += order.price

        # pass total number of orders and total revenue into template
        context = {
            'orders': orders,
            # 'total_revenue': total_revenue,
            'total_orders': total_orders
        }

        return render(request, 'restaurant/index.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class OrderDetails(View):
    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(OrderPlaced, pk=pk)
        context = {
            'order': order
        }
        return render(request, 'restaurant/order_details.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(OrderPlaced, pk=pk)
        order.is_served = True
        order.save()
        return redirect('order_details', pk=pk)
    
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
        reservation_id = request.POST.get('reservation_id')  # Assuming the hidden input is named 'reservation_id'
        reservation = ReservationModel.objects.get(pk=reservation_id)
        # reservation = ReservationModel.objects.get(pk=pk)
        reservation.is_served = True
        reservation.save()
        context = {
            'reservation':reservation
        }

        return redirect('reservation_details', pk=pk)
    
class MarkAsServed(View):
    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(OrderPlaced, pk=order_id)
        order.is_served = True
        order.save()
        # Optionally, redirect to a different URL or render a template
        return redirect('restaurant_index')
    
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        sales_per_item = [{'product': product, 'total_sales': product.price * product.quantity_sold} for product in products]
        total_revenue = sum(item['total_sales'] for item in sales_per_item)
        return render(request, 'restaurant/dashboard.html', {'sales_per_item': sales_per_item, 'total_revenue': total_revenue})
