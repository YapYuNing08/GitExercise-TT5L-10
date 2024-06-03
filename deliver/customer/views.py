from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.views import View
from django.db.models import Q
from .models import MenuItem, Category, OrderModel, Product, OrderItem, Customer, Cart, ReservationModel, OrderPlaced, Product, CustomizationChoice
from .forms import CustomerRegistrationForm, CustomerProfileForm, CustomizationForm
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse


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
        total_amount = sum(item.total_cost for item in cart_items)
        
        context = {
            'add': add,
            'cart_items': cart_items,
            'total_amount': total_amount
        }
        return render(request, 'customer/checkout.html', context)

def order_placed(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user).select_related('product').prefetch_related('customizations')

    ordered_items = []
    for item in cart_items:
        order = OrderPlaced.objects.create(
            user=user,
            product=item.product,
            quantity=item.quantity,
            status='Pending'
        )
        order.customizations.set(item.customizations.all())
        order.save()
        ordered_items.append(order)

    cart_items.delete()
    return render(request, 'customer/order_summary.html', {'ordered_items': ordered_items})


def order_history(request):
    order_placed = OrderPlaced.objects.filter(user=request.user).prefetch_related('customizations')
    return render(request, 'customer/order_history.html', {'order_placed': order_placed})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id') 
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
   
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()

        else:
            Cart.objects.create(user=request.user, product_id=prod_id, quantity=1)
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
                'totalamount': amount,  # Assuming totalamount is the same as amount in this context
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
            cart_item_quantity = cart_item.quantity  # Store the quantity before deletion
            cart_item.delete()  # Delete the cart item

            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.price for item in cart)
            # totalamount = amount  # Assuming totalamount is the same as amount in this context
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


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html')
    
# class PasswordResetView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'customer/login.html')
    

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
    