from django.contrib import admin
from .views import *
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('', views.register , name="register"),
    path('login/' , views.login , name='login'),
    path('logout/' , views.user_logout , name='logout'),
    path('test/' , views.test , name='test'),
    path('staff/' , views.staff , name='staff'),
    path('top/' , views.top , name='top'),
    path('product/' , views.product , name='product'),
    path('order/' , views.order , name='order'),
    path('profile/' , views.profile , name='profile'),
    path('delete/<int:pk>/' , views.delete , name='delete'),
    path('staff_details/<int:pk>/' , views.staff_details , name='staff_details'),
    path('product_update/<int:pk>/' , views.product_update , name='product_update'),
    path('profile_update/' , views.profile_update , name='profile_update'),
    path('checkout/' , views.checkout , name='checkout'),
    path('cart/' , views.cart , name='cart'),
    path('addto_cart/<int:product_id>/', views.addto_cart, name='addto_cart'),
    path('delete_cart_item/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('success/', views.success, name='success'), 
    path('cancel/', views.cancel, name='cancel'), 
    path('process-checkout/', ProcessCheckoutView.as_view(), name='process_checkout'),
    path('stripe/webhook/', views.payment_webhook, name='payment_webhook'),
    path('myorder/', views.myorder, name='myorder'),
    path('Lowstock/' , views.Lowstock  , name='Lowstock'),
    # path('saved_cards/' , views.saved_cards  , name='saved_cards'),
    path('get-order-data/', views.get_order_data, name='get_order_data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)