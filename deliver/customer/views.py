from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from .models import MenuItem, OrderModel, Product, OrderItem, Customer, Cart, ReservationModel, OrderPlaced, RedemptionOption, RedeemedItem
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
    
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
        return render(request, 'customer/about.html')

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
        

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        beverage = MenuItem.objects.filter(category__name__contains='Beverage')
        desserts = MenuItem.objects.filter(category__name__contains='Desserts')
        pastries = MenuItem.objects.filter(category__name__contains='Pastries')
        main = MenuItem.objects.filter(category__name__contains='Main')
        

        # pass into context
        context = {
            'beverage': beverage,
            'desserts': desserts,
            'pastries': pastries,
            'main': main
            
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        items_ids = request.POST.getlist('items[]')
        quantities = request.POST.getlist('quantities[]')
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        total_price = 0
        items_with_quantity = []  
        for item_id, quantity in zip(items_ids, quantities):
            item = MenuItem.objects.get(id=item_id)
            item_total_price = item.price * int(quantity)
            if item_total_price > 0:
                items_with_quantity.append({'item': item, 'quantity': int(quantity), 'total_price': item_total_price})  
                total_price += item_total_price

        order = OrderModel.objects.create(
            price=total_price,
            name=name,
            phone=phone,
        )

        # Create OrderItem instances for each selected item
        for item_info in items_with_quantity:
            order_item = OrderItem.objects.create(
                order=order,
                item=item_info['item'],
                quantity=item_info['quantity'],
                total_price=item_info['total_price']
            )

        context = {
            'items_with_quantity': items_with_quantity,
            'total_price': total_price
        }

        return render(request, 'customer/order_history.html', context)



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
    
class Menu(View):
    def get(self, request, *args, **kwargs):
        # Retrieve menu items from the database
        menu_items = MenuItem.objects.all()
        context = {'menu_items': menu_items}

        return render(request, 'customer/menu.html', context)

def all_products(request):
    # categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'customer/all_products.html', {'products': products})


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
        product = Product.objects.get(pk=pk)
        return render(request, 'customer/product_detail.html', locals())
    
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
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def show_cart(request):
    user = request.user  
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.price
        amount = amount + value
    totalamount = amount
    return render(request, 'customer/addtocart.html', locals())


class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        
        # Calculate total price for each item and overall total
        cart_items_with_total = []
        for p in cart_items:
            total_price = p.quantity * p.product.price
            famount += total_price
            cart_items_with_total.append({
                'product': p.product,
                'quantity': p.quantity,
                'total_price': total_price
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
        num_items = len(request.POST) // 2  # Divide by 2 because each item has 2 hidden inputs
        for i in range(1, num_items + 1):
            product_id = request.POST.get('product_id_' + str(i))  # Get the product ID for the current item
            quantity = request.POST.get('quantity_' + str(i))  # Get the quantity for the current item
            
            cart_item = Cart.objects.filter(user=user, product_id=product_id).first()
            if cart_item:
                OrderPlaced.objects.create(user=user, product=cart_item.product, quantity=quantity, status='Pending')
                cart_item.delete()  # Remove the cart item after ordering
        
        return redirect('order_history')  # Redirect to the order confirmation page

    return redirect('checkout')  # Redirect to the checkout page if the request method is not POST

def order_placed(request):
    if request.method == 'POST':
        user = request.user
        num_items = len(request.POST) // 2  # Divide by 2 because each item has 2 hidden inputs
        ordered_items = []

        total_points = 0  # Initialize total points for the order

        for i in range(1, num_items + 1):
            product_id = request.POST.get('product_id_' + str(i))  # Get the product ID for the current item
            quantity = int(request.POST.get('quantity_' + str(i)))  # Get the quantity for the current item

            cart_item = Cart.objects.filter(user=user, product_id=product_id).first()
            if cart_item:
                ordered_items.append({
                    'product': cart_item.product,
                    'quantity': quantity,
                    'total_price': cart_item.product.price * quantity
                })

                # Calculate points based on the total price of the item
                item_points = int(cart_item.product.price)  # Example: 1 point per dollar spent
                total_points += item_points * quantity

                # Increment the quantity_sold field in the Product model
                cart_item.product.quantity_sold += quantity
                cart_item.product.save()

                OrderPlaced.objects.create(user=user, product=cart_item.product, quantity=quantity, status='Pending', points=item_points)
                cart_item.delete()  # Remove the cart item after ordering

        user_profile, created = Customer.objects.get_or_create(user=request.user)
        initial_points = user_profile.points

        user_profile.points += total_points  # Add the earned points
        user_profile.save()

        # Pass the ordered items and total points to the new HTML page
        context = {'ordered_items': ordered_items, 'total_points': total_points, 'initial_points': initial_points}
        return render(request, 'customer/order_summary.html', context)  # Render the order summary page

    return redirect('checkout')  # Redirect to the checkout page if the request method is not POST

def order_history(request):
    order_placed=OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'customer/order_history.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id') 
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = Cart.objects.create(user=request.user, product_id=prod_id, quantity=1)

        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.price for item in cart)
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': amount,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id') 
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.quantity -= 1
            cart_item.save()

            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.price for item in cart)
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': amount,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found for the user and product.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        if cart_item:
            cart_item_quantity = cart_item.quantity
            cart_item.delete()

            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.price for item in cart)
            data = {
                'quantity': cart_item_quantity,
                'amount': amount,
                'totalamount': amount,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found for the user and product.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html')
    

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'customer/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']

            reg = Customer(user=user, name=name, mobile=mobile)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully.")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'customer/profile.html', locals())



def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'customer/address.html', locals())



class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'customer/updateAddress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.mobile = form.cleaned_data['mobile']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully.")
        else:
            messages.warning(request, "Invalid Input Data.")
        return redirect('address')
    
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
        option = RedemptionOption.objects.get(pk=option_id)
        
        customer = request.user.customer
        if customer.points >= option.points_required:
            # Deduct points
            customer.points -= option.points_required
            customer.save()
            
            # Record the redemption
            RedeemedItem.objects.create(customer=customer, option=option)
            
            # Add success message
            messages.success(request, f"Successfully redeemed {option.name}!")
        else:
            messages.error(request, "You do not have enough points to redeem this item.")
        
        return redirect('point')

def verify_item(request):
    if request.method == 'POST':
        redemption_id = request.POST.get('redemption_id')
        admin_password = request.POST.get('admin_password')
        try:
            # Retrieve the superuser with username 'admin'
            superuser = User.objects.get(username='admin')

            # Check if the provided password matches the superuser's password
            if check_password(admin_password, superuser.password):
                # Assuming Redemption model has a foreign key to the user who redeemed it
                redemption = RedeemedItem.objects.get(id=redemption_id)
                # Remove the item from redeemed items
                redemption.delete()
                # Your verification logic here
                messages.success(request, 'Item has been claimed successfully.')
                # Redirect or render your response
                return redirect('point')
            else:
                # Incorrect password, display error message
                messages.error(request, 'Incorrect admin password. Please try again.')
                # Redirect or render your response
                return redirect('point')
            
        except User.DoesNotExist:
            # Handle if the superuser 'admin' does not exist
            messages.error(request, 'Admin user not found.')
            # Redirect or render your response
            return redirect('point')

    return redirect('point')  # Redirect back to the rewards page if not a POST request