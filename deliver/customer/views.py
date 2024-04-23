from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        coffee = MenuItem.objects.filter(category__name__contains='Coffee')
        tea = MenuItem.objects.filter(category__name__contains='Tea')
        pastries = MenuItem.objects.filter(category__name__contains='Pastries')
        desserts = MenuItem.objects.filter(category__name__contains='Desserts')

        # pass into context
        context = {
            'coffee': coffee,
            'tea': tea,
            'pastries': pastries,
            'desserts': desserts,
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
                f'Your total: {price}\n')
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







