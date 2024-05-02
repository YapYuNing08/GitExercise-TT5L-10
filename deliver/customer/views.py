from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import MenuItem, Category, OrderModel, ReservationModel
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class Reservation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/reservation.html')
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        date = request.POST.get('date')
        person = request.POST.get('person')
        
        reservation = ReservationModel.objects.create(name=name,email=email,number=number,date=date,person=person)
        reservation.save()
        return redirect('reservation')

        # return render(request, 'customer/reservation.html')

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
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        # order_items = {
        #     'items': []
        # }

        items = MenuItem.objects.filter(id__in=items_ids)

        # for item in items:
        #     menu_item = MenuItem.objects.get(pk__contains=int(item))
        #     item_data = {
        #         'id': menu_item.pk,
        #         'name': menu_item.name,
        #         'price': menu_item.price
        #     }

        #     order_items['items'].append(item_data)

        #     price = 0
        #     item_ids = []
        total_price = sum(item.price for item in items)

        # for item in order_items['items']:
        #     price += item['price']
        #     item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=total_price,
            name=name,
            phone=phone,
        )
        order.items.set(items)

        # Send confirmation email to the user
        # body = ('Thank you for your order! Your food is being made and will be served soon!\n'
        #         f'Your total: RM{price}\n')
        # send_mail(
        #     'Thank You For Your Order!',
        #     body,
        #     'example@example.com',
        #     [email],
        #     fail_silently=False
        # )


        context = {
            'items': items,
            'price': total_price
        }

        return render(request, 'customer/order_confirmation.html', context)






