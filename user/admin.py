from django.contrib import admin
from .models import Product, Order, Profile, ShippingAddress, OrderItem

# Customization for the Product model in the admin interface
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category', 'new_arrival')
    list_filter = ['category' ,'new_arrival' ]

# Customization for the Order model in the admin interface
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'product_name', 'product_quantity', 'date', 'payment_status')

    def product_name(self, obj):
        # Display product names in the order
        return ", ".join([item.product.name for item in obj.orderitem_set.all()])
    product_name.short_description = "Product Name"

    def product_quantity(self, obj):
        # Display quantities of the products in the order
        return ", ".join([str(item.quantity) for item in obj.orderitem_set.all()])
    product_quantity.short_description = "Product Quantity"

# Register models with their respective admin customizations
admin.site.site_header = "Inventory Admin Panel"
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(ShippingAddress)
