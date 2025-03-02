from django.contrib import admin
from .views import *
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('' , views.test , name='test'),
    path('register/', views.register , name="register"),
    path('login/' , views.login , name='login'),
    path('logout/' , views.user_logout , name='logout'),
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
    path('get-order-data/', views.get_order_data, name='get_order_data'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('faq/', views.faq, name='faq'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)