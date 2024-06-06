"""
URL configuration for deliver project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import Index, About, Order, Signin, Signup, Menu, MenuSearch, Category, CategoryTitle, ProductDetail, CustomerRegistrationView, Login, ProfileView, Reservation, ReservationConfirmation, Logout, Checkout
from django.contrib.auth import views as auth_view
from customer.forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm
from customer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('', Signin.as_view(), name="signin"),
    path('index/', Index.as_view(), name='index'),
    path('about/', About.as_view(), name="about"),
    path('point/', views.point, name='point'),
    path('redeem_item/', views.redeem_item, name='redeem_item'),
    path('claim_item/', views.claim_item, name='claim_item'), 

    path('reservation/', Reservation.as_view(), name='reservation'),
    path('reservation_confirmation/', ReservationConfirmation.as_view(), name='reservation_confirmation'),
    
    path('signup/', Signup.as_view(), name="signup"),

    path('order/', Order.as_view(), name="order"),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search', MenuSearch.as_view(), name='menu-search'),
    path('all-products/', views.all_products, name='all_products'),
    path('order_again/<int:order_id>/', views.order_again, name='order_again'),
    
    path("category/<slug:val>", Category.as_view(), name="category"),
    path("category_title/<val>", CategoryTitle.as_view(), name="category_title"),

    path('product_detail/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_info/', views.profile_info_view, name='profile_info'),
    
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', Checkout.as_view(), name='checkout'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('order_placed/', views.order_placed, name='order_placed'), 
    path('order_history/', views.order_history, name='order_history'),
    path('order_again/<int:order_id>/', views.order_again, name='order_again'),

    # login authentication
    path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='customer/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password_change/', auth_view.PasswordChangeView.as_view(template_name='customer/changepassword.html', form_class=MyPasswordChangeForm),name='password_change'),
    path('password_change_done/', auth_view.PasswordChangeDoneView.as_view(template_name='customer/passwordchangedone.html'), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)