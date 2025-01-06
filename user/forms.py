from django.contrib.auth.forms import UserCreationForm 
from django import forms
from .models import Product
from django.contrib.auth.models import User
from .models import Profile , Order , OrderItem


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' , 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address' , 'phone' , 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= ['name' , 'category' , 'quantity' ,'price' , 'description' , 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product' , 'order_quantity']
        