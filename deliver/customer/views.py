from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.db.models import Q
from .models import MenuItem, Category, OrderModel, Product, OrderItem, Customer, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
# class Dashboard(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'customer/dashboard.html')

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
        
        my_user = User.objects.create_user(uname,email,pass1)
        my_user.save()
        return redirect('signin')
        
class Signin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/signin.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        print(username,pass1)

        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse("Username or Password is incorrect!")
        

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

        return render(request, 'customer/order_confirmation.html', context)



class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        if query:
            menu_items = MenuItem.objects.filter(
                Q(name__icontains=query) |
                Q(price__icontains=query) |
                Q(description__icontains=query)
            )
        else:
            menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items,
            'query': query
        }

        return render(request, 'customer/menu.html', context)
    
class Menu(View):
    def get(self, request, *args, **kwargs):
        # Retrieve menu items from the database
        menu_items = MenuItem.objects.all()
        context = {'menu_items': menu_items}

        return render(request, 'customer/menu.html', context)
    
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
    user=request.user
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


# def checkout(View):
#     def get(self, request):
#         return render(request, 'customer/checkout.html', locals())



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)




class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html')
    
# class PasswordResetView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'customer/login.html')
    

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
            address = form.cleaned_data['address']

            reg = Customer(user=user, name=name, mobile=mobile, address=address)
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
            add.address = form.cleaned_data['address']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully.")
        else:
            messages.warning(request, "Invalid Input Data.")
        return redirect('address')
    
