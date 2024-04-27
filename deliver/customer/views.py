from django.shortcuts import render, redirect
from django.views import View
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login



def home(request):
    return render(request, 'customer/home.html')

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # if User.objects.filter(username=username):
        #     messages.error(request, "Username already exist! Please try some other username")
        #     return redirect ('home')
        
        # if User.objects.filter(email=email):
        #     messages.error(request, "Email already registered! Please try some other email")
        #     return redirect ('home')
        
        # if len(username)>0:
        #     messages.error(request, "Username must be under 10 characters")

        # if not username.isalnum():
        #     messages.error(request, "Username must be Alpha-Numeric")
        #     return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        # messages.success(request, "Your Account has been successfully created")

        return redirect('signin')

    return render(request, 'customer/signup.html', )

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 =request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "customer/index.html", {"fname":fname})

        else:
            # messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request, 'customer/signin.html')


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    
# class Signin(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'customer/signin.html')
    
# class Signup(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'customer/signup.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        # coffee = MenuItem.objects.filter(category__name__contains='Coffee')
        beverage = MenuItem.objects.filter(category__name__contains='Beverage')
        # pastries = MenuItem.objects.filter(category__name__contains='Pastries')
        desserts = MenuItem.objects.filter(category__name__contains='Desserts')
        pastries = MenuItem.objects.filter(category__name__contains='Pastries')
        main = MenuItem.objects.filter(category__name__contains='Main')
        

        # pass into context
        context = {
            # 'coffee': coffee,
            'beverage': beverage,
            # 'pastries': pastries,
            'desserts': desserts,
            'pastries': pastries,
            'main': main
            
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email
        )
        order.items.add(*item_ids)

        # Send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be served soon!\n'
                f'Your total: RM{price}\n')
        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )


        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)






