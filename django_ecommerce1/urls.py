"""
URL configuration for django_ecommerce1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from products import views as products_views
from carts import views as carts_views
from orders import views as orders_views
from marketing import views as marketing_views
from accounts import views as accounts_views

urlpatterns = [
    path('', products_views.home, name='home'),
    path('s/', products_views.search, name='search'),
    path('products/', products_views.all, name='products'),
    re_path(r'^products/(?P<slug>[\w-]*)/$', products_views.single, name='single_product'),
    re_path(r'^cart/(?P<id>\d+)/$', carts_views.remove_from_cart, name='remove_from_cart'),
    re_path(r'^cart/(?P<slug>[\w-]*)/$', carts_views.add_to_cart, name='add_to_cart'),
    path('cart/', carts_views.view, name='cart'),
    path('checkout/', orders_views.checkout, name='checkout'),
    path('orders/', orders_views.orders, name='user_orders'),
    path('ajax/dismiss_marketing_message/', marketing_views.dismiss_marketing_message, name='dismiss_marketing_message'),
    path('ajax/email_signup/', marketing_views.email_signup, name='ajax_email_signup'),
    path('ajax/add_user_address/', accounts_views.add_user_address, name='ajax_add_user_address'),

    path('admin/', admin.site.urls),
    path('accounts/logout/', accounts_views.logout_view, name='auth_logout'),
    path('accounts/login/', accounts_views.login_view, name='auth_login'),
    path('accounts/register/', accounts_views.registration_view, name='auth_register'),
    path('accounts/address/add/', accounts_views.add_user_address, name='add_user_address'),
    re_path(r'^accounts/activate/(?P<activation_key>\w+)/$', accounts_views.activation_view, name='activation_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
