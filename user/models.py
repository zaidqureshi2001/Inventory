from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
CATEGORY = (
    ('Stationary' , 'Stationary'),
    ('Electronics' , 'Electronics'),
    ('Food' , 'Food'),
    ('Dress' , 'Dress'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True , default='Untitled Product')
    category = models.CharField(max_length=20, choices=CATEGORY, blank=True ,default='Stationary')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , null=True )
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True , related_name='shipping_addresses')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(
        max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')],
        default='failed'
    )
    
    def __str__(self):
        return f'{self.product} order by {self.staff.username}'

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)  # Added state
    zipcode = models.CharField(max_length=20)  # Added zipcode
    phone_no = models.CharField(max_length=20 , null=True , blank=True)
    
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='shipping_addresses')  # Add related_name

    def __str__(self):
        if self.customer:
            return f"{self.customer.username}'s address"
        return "No customer"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
  
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='Profile_Images')
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_method_id = models.CharField(max_length=255, blank=True, null=True)  # Add this line

    def __str__(self):
        return f'{self.staff.username}--Profile'
