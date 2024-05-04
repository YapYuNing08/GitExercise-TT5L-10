from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.db.models import Q
from .models import MenuItem, Category, OrderModel, OrderItem, Product
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# from customer import views

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

    # def post(self, request, *args, **kwargs):
    #     items_ids = request.POST.getlist('items[]')
    #     name = request.POST.get('name')
    #     phone = request.POST.get('phone')

    #     # order_items = {
    #     #     'items': []
    #     # }

    #     items = MenuItem.objects.filter(id__in=items_ids)

    #     # for item in items:
    #     #     menu_item = MenuItem.objects.get(pk__contains=int(item))
    #     #     item_data = {
    #     #         'id': menu_item.pk,
    #     #         'name': menu_item.name,
    #     #         'price': menu_item.price
    #     #     }

    #     #     order_items['items'].append(item_data)

    #     #     price = 0
    #     #     item_ids = []
    #     total_price = sum(item.price for item in items)

    #     # for item in order_items['items']:
    #     #     price += item['price']
    #     #     item_ids.append(item['id'])

    #     order = OrderModel.objects.create(
    #         price=total_price,
    #         name=name,
    #         phone=phone,
    #     )
    #     order.items.set(items)

    #     # Send confirmation email to the user
    #     # body = ('Thank you for your order! Your food is being made and will be served soon!\n'
    #     #         f'Your total: RM{price}\n')
    #     # send_mail(
    #     #     'Thank You For Your Order!',
    #     #     body,
    #     #     'example@example.com',
    #     #     [email],
    #     #     fail_silently=False
    #     # )

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
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
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