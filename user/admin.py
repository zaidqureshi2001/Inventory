from django.contrib import admin
from .models import Product , Order , Profile , ShippingAddress , OrderItem
# Register your models here.
admin.site.site_header = "Inventory Admin_panel"


class productadmin(admin.ModelAdmin):
    list_display = ('name' , 'quantity' ,'category' ,)
    list_filter = ['category']


admin.site.register(Product, productadmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(ShippingAddress)