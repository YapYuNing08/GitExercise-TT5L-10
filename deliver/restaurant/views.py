from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.utils.timezone import datetime
from customer.models import ReservationModel, OrderPlaced, Product, RedeemedItem
from django.contrib import messages

class Index(View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderPlaced.objects.filter(
            ordered_date__year=today.year, ordered_date__month=today.month, ordered_date__day=today.day).order_by('-ordered_date')
        
        # loop through the orders and add the price value

        total_orders = len(orders)

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
        today = datetime.today().date()

        products = Product.objects.all()

        # Calculate overall total sales per item and total revenue
        sales_per_item = [{'product': product, 'total_sales': product.price * product.quantity_sold} for product in products]
        total_revenue = sum(item['total_sales'] for item in sales_per_item)

        # Filter order items for today
        order_items_today = OrderPlaced.objects.filter(ordered_date__date=today)

        # Calculate sales per item and total revenue for today
        sales_per_item_today = []
        for product in products:
            quantity_sold_today = sum(item.quantity for item in order_items_today if item.product == product)
            total_sales_today = sum(item.quantity * item.product.price for item in order_items_today if item.product == product)
            sales_per_item_today.append({
                'product': product,
                'quantity_sold_today': quantity_sold_today,
                'total_sales_today': total_sales_today
            })
        
        total_revenue_today = sum(item['total_sales_today'] for item in sales_per_item_today)

        context = {
            'sales_per_item': sales_per_item,
            'total_revenue': total_revenue,
            'sales_per_item_today': sales_per_item_today,
            'total_revenue_today': total_revenue_today
        }

        return render(request, 'restaurant/dashboard.html', context)

def update_food_status(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('food_status')
        order.food_status = new_status
        order.save()
        return redirect('restaurant_index')  # Redirect to the index page after updating
    return render(request, 'restaurant/update_food_status.html', {'order': order})

def verify_claim(request):
    verification_result = ''
    verified_redemption_id = None

    if request.method == 'POST':
        redemption_id = request.POST.get('redemption_id')
        claim_code = request.POST.get('claim_code')
        try:
            item = RedeemedItem.objects.get(id=redemption_id)
            if item.claim_code == claim_code:
                item.claimed = True
                item.save()
                verification_result = 'success'
                verified_redemption_id = redemption_id
            else:
                verification_result = 'incorrect_code'
        except RedeemedItem.DoesNotExist:
            verification_result = 'invalid_id'

    all_items = RedeemedItem.objects.all().order_by('-id')
    return render(request, 'restaurant/verify_claim.html', {
        'all_items': all_items,
        'verification_result': verification_result,
        'verified_redemption_id': verified_redemption_id
    })