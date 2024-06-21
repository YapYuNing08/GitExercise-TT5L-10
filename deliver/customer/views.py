from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
import random
from django.views import View
from django.db.models import Q
from .models import Product, Customer, Cart, ReservationModel, OrderPlaced, Product, CustomizationChoice, RedemptionOption, RedeemedItem, Ad
from .forms import CustomerRegistrationForm, CustomerProfileForm, CustomizationForm, ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class Reservation(View):
    def get(self, request, *args, **kwargs):
        reservations = ReservationModel.objects.all()
        return render(request, 'customer/reservation.html')
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        person = request.POST.get('person')
        
        reservation = ReservationModel.objects.create(
            name=name,      
            phone=phone,
            date=date,
            time=time,
            person=person)
        
        reservation.save()
        request.session['reservation_id'] = reservation.id
        
        return redirect('reservation_confirmation')
    
class ReservationConfirmation(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the reservation ID from the session
        reservation_id = request.session.get('reservation_id')
        if reservation_id is None:
            return HttpResponse("Reservation ID not found in session.")
        
        # Get the reservation object
        reservation = ReservationModel.objects.get(pk=reservation_id)
        
        context = {
            'reservation': reservation
        }
        return render(request, 'customer/reservation_confirmation.html', context)

class About(View):
    def get(self, request, *args, **kwargs):
        ad = Ad.objects.filter(is_active=True).first()
        return render(request, 'customer/about.html', {'ad': ad})

class Signup(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/signup.html')
        
    def post(self, request, *args, **kwargs):
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Passwords do not match")
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("This email is already in use. Please use a different email.")
        
        if User.objects.filter(username=uname).exists():
            return HttpResponse("This username is already in use. Please use a different username.")
        
        if 'admin' in uname:
            return HttpResponse("Username 'admin' is not allowed. Please try again with a different username.")
        
        my_user = User.objects.create_user(uname,email,pass1)
        my_user.save()
        return redirect('signin')
        
class Signin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/signin.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
       

        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            Customer.objects.get_or_create
            if 'admin' in username:
                login(request,user)
                return redirect('restaurant_index')
            else:
                login(request,user)
                return redirect('about')
        else:
            return HttpResponse("Username or Password is incorrect!")

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Logs out the user
        return redirect('signin') 


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        if query:
            products = Product.objects.filter(
                Q(title__icontains=query) |
                Q(price__icontains=query) 
            )
        else:
            products = Product.objects.all()

        context = {
            'products': products,
            'query': query
        }

        return render(request, 'customer/all_products.html', context)


def all_products(request):
    # categories = Category.objects.all()
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(title__icontains=query)

    latest_orders = OrderPlaced.objects.filter(user=request.user).order_by('-id')[:2]

    return render(request, 'customer/all_products.html', {'products': products, 'latest_orders': latest_orders})


class Category(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "customer/category.html", locals())

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "customer/category.html", locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CustomizationForm(product=product)
        return render(request, 'customer/product_detail.html', {'product': product, 'form': form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CustomizationForm(request.POST, product=product)
        if form.is_valid():
            selected_customizations = []
            for option_name, choice_id in form.cleaned_data.items():
                choice = CustomizationChoice.objects.get(id=choice_id)
                selected_customizations.append(choice.id)

            request.POST = request.POST.copy()
            request.POST.setlist('customization_choices', selected_customizations)
            request.POST['prod_id'] = product.id  # Ensure prod_id is included in POST data

            return add_to_cart(request)
        return render(request, 'customer/product_detail.html', {'product': product, 'form': form})

    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customer/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulation! User Register successfully')
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'customer/customerregistration.html', locals())

def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        customization_choice_ids = request.POST.getlist('customization_choices')
        customization_choices = CustomizationChoice.objects.filter(id__in=customization_choice_ids)

        cart_item = None
        for item in Cart.objects.filter(user=user, product=product):
            if set(item.customizations.values_list('id', flat=True)) == set(customization_choice_ids):
                cart_item = item
                break

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart.objects.create(user=user, product=product, quantity=1)
            cart_item.customizations.set(customization_choices)

        cart_item.save()

        return redirect('showcart')
    return HttpResponse("This endpoint only accepts POST requests.")

def show_cart(request):
    user = request.user  
    cart = Cart.objects.filter(user=user).select_related('product').prefetch_related('customizations')
    total_amount = sum(item.total_cost for item in cart)
    return render(request, 'customer/addtocart.html', {'cart': cart, 'total_amount': total_amount})

class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user).select_related('product').prefetch_related('customizations')

        famount = 0
        cart_items_with_total = []
        for p in cart_items:
            total_price = p.quantity * p.product.price
            customizations_total = sum(c.additional_price for c in p.customizations.all())
            total_price += customizations_total * p.quantity  # Include customization price for each item quantity
            famount += total_price
            cart_items_with_total.append({
                'product': p.product,
                'quantity': p.quantity,
                'total_price': total_price,
                'customizations': p.customizations.all()
            })

        totalamount = famount
        context = {
            'add': add,
            'cart_items_with_total': cart_items_with_total,
            'totalamount': totalamount
        }
        return render(request, 'customer/checkout.html', context)

def order_placed(request):
    if request.method == 'POST':
        user = request.user
        method = request.POST.get('method')
        order_id = generate_order_id()

        if not method:
            return redirect('checkout')

        table_number = request.POST.get('table_number') if method == 'Dine In' else None

        num_items = (len(request.POST) - 2) // 2  # Adjusting for additional fields like method and order_id
        ordered_items = []
        total_points = 0

        for i in range(1, num_items + 1):
            product_id = request.POST.get(f'product_id_{i}')
            quantity_str = request.POST.get(f'quantity_{i}')
            if quantity_str is not None:
                quantity = int(quantity_str)
            else:
                quantity = 0

            cart_item = Cart.objects.filter(user=user, product_id=product_id).first()
            if cart_item:
                total_item_price = cart_item.product.price + sum(c.additional_price for c in cart_item.customizations.all())
                total_price = total_item_price * quantity

                order = OrderPlaced.objects.create(
                    user=user,
                    product=cart_item.product,
                    quantity=quantity,
                    food_status='Pending',
                    method=method,
                    points=0,
                    table_number=table_number,
                    order_id=order_id
                )
                order.customizations.set(cart_item.customizations.all())
                order.save()

                ordered_items.append({
                    'product_id': cart_item.product.id,
                    'title': cart_item.product.title,
                    'price': total_item_price,
                    'quantity': quantity,
                    'total_price': total_price,
                    'is_served': False,
                    'customizations': list(cart_item.customizations.all())
                })

                item_points = int(total_item_price) * quantity
                total_points += item_points

                cart_item.product.quantity_sold += quantity
                cart_item.product.save()

                order.points = item_points
                order.save()

                cart_item.delete()

        user_profile, created = Customer.objects.get_or_create(user=request.user)
        initial_points = user_profile.points

        user_profile.points += total_points
        user_profile.save()

        context = {
            'ordered_items': ordered_items,
            'total_points': total_points,
            'initial_points': initial_points,
            'method': method,
            'table_number': table_number,
            'order_id': order_id
        }
        return render(request, 'customer/order_summary.html', context)
    else:
        return redirect('checkout')



def generate_order_id():
    # Implement your logic to generate a unique order ID here
    return 'ORD' + str(random.randint(100, 999))

def order_history(request):
    order_placed = OrderPlaced.objects.filter(user=request.user).prefetch_related('customizations').order_by('-ordered_date')
    return render(request, 'customer/order_history.html', {'order_placed': order_placed})

def plus_cart(request):
    if request.method == 'GET':
        cart_item_id = request.GET.get('cart_item_id') 
        cart_item = Cart.objects.filter(Q(id=cart_item_id) & Q(user=request.user)).first()
   
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
            
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.price for item in cart)
        data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': amount,  # Assuming totalamount is the same as amount in this context
            }

        return JsonResponse(data) 
                
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def minus_cart(request):
    if request.method == 'GET':
        cart_item_id = request.GET.get('cart_item_id') 
        cart_item = Cart.objects.filter(Q(id=cart_item_id) & Q(user=request.user)).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.price for item in cart)
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': amount,  # Assuming totalamount is the same as amount in this context
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found for the user and product.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def remove_cart(request):
    if request.method == 'GET':
        cart_item_id = request.GET.get('cart_item_id') 
        cart_item = Cart.objects.filter(Q(id=cart_item_id) & Q(user=request.user)).first()
        if cart_item:
            cart_item_quantity = cart_item.quantity  # Store the quantity before deletion
            cart_item.delete()  # Delete the cart item

            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.price for item in cart)
            data = {
                'quantity': cart_item_quantity,  # Use the stored quantity before deletion
                'amount': amount,
                'totalamount': amount,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found for the user and product.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)



class ProfileView(View):
    def get(self, request):
        customer = request.user.customer
        form = CustomerProfileForm(instance=customer)
        return render(request, 'customer/profile.html', {'form': form})

    def post(self, request):
        customer = request.user.customer
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile_info')
        return render(request, 'customer/profile.html', {'form': form})
    
def profile_info_view(request):
    customer = request.user.customer
    return render(request, 'customer/profile_info.html', {'customer': customer})

    
def point(request):
    user_profile, created = Customer.objects.get_or_create(user=request.user)
    initial_points = user_profile.points
    redemption_options = RedemptionOption.objects.all()
    redeemed_items = RedeemedItem.objects.filter(customer=user_profile)
    context = {'initial_points': initial_points, 'redemption_options': redemption_options, 'redeemed_items': redeemed_items}
    return render(request, 'customer/point.html', context)

def redeem_item(request):
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        option = get_object_or_404(RedemptionOption, id=option_id)
        product = get_object_or_404(Product, title=option.name)
        customer = request.user.customer
        today = timezone.now().date()  # Use timezone.now() to get the current date and time

        # Check if the user has already redeemed this product today and if it requires a review
        already_redeemed = RedeemedItem.objects.filter(customer=customer, option=option, date_redeemed__date=today).exists()

        if already_redeemed:
            messages.error(request, 'You have already redeemed this item today.')
        else:
            if option.points_required == 0 and RedeemedItem.objects.filter(customer=customer, option=option, date_redeemed__date=today).exists():
                messages.error(request, 'You can only redeem this item once per day.')
            elif option.review_required:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.customer = customer
                    review.product = product
                    review.save()
                    messages.success(request, 'Thank you for your review! Item redeemed successfully!')
                    RedeemedItem.objects.create(customer=customer, option=option, date_redeemed=timezone.now())
                else:
                    messages.error(request, 'There was an error with your review. Please try again.')
            else:
                if customer.points >= option.points_required:
                    customer.points -= option.points_required
                    customer.save()
                    RedeemedItem.objects.create(customer=customer, option=option, date_redeemed=timezone.now())
                    messages.success(request, 'Item redeemed successfully!')
                else:
                    messages.error(request, 'Not enough points to redeem this item.')

    return redirect('point')

def claim_item(request):
    if request.method == 'POST':
        redemption_id = request.POST.get('redemption_id')
        
        try:
            redemption = RedeemedItem.objects.get(id=redemption_id)
            if not redemption.claimed:
                redemption.generate_claim_code()  # Generate and save the claim code
                redemption.save()
                messages.success(request, f'Item has been claimed successfully. Your verification code is {redemption.claim_code}. Show this code to admin!')
            else:
                messages.error(request, 'Item has already been claimed.')
        except RedeemedItem.DoesNotExist:
            messages.error(request, 'Invalid redemption ID.')

        return redirect('point')
    else:
        return redirect('point')

def order_again(request, order_id):
    previous_order = get_object_or_404(OrderPlaced, id=order_id, user=request.user)
    customizations = previous_order.customizations.all()

    # Check if a similar cart item exists
    cart_item = Cart.objects.filter(
        user=request.user,
        product=previous_order.product,
        customizations__in=customizations
    ).first()

    if cart_item:
        # If a similar cart item exists, update its quantity
        cart_item.quantity += previous_order.quantity
        cart_item.save()
    else:
        # If no similar cart item exists, create a new one
        cart_item = Cart.objects.create(
            user=request.user,
            product=previous_order.product,
            quantity=previous_order.quantity,
        )

        # Set customizations for the new cart item
        cart_item.customizations.set(customizations)

    return redirect('/cart')

