
"""
URL configuration for deliver project.

The `urlpatterns` list routes URLs to views. For more information please see:
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
from customer.views import Index, About, Order, Signin, Signup, Reservation, Category, CategoryTitle, ProductDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('', Signin.as_view(), name="signin"),
    path('index/', Index.as_view(), name='index'),
    path('reservation/', Reservation.as_view(), name='reservation'),
    path('about/', About.as_view(), name="about"),
    path('signup/', Signup.as_view(), name="signup"),
    path('order/', Order.as_view(), name="order"),
    path("category/<slug:val>", Category.as_view(), name="category"),
    path("category_title/<val>", CategoryTitle.as_view(), name="category_title"),
    path("product_detail/<int:pk>", ProductDetail.as_view(), name="product_detail")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

