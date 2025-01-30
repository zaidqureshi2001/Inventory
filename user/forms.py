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
        fields= ['name' , 'category' , 'quantity' ,'price' , 'fake_price',  'description' , 'image']
        
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        fake_price = cleaned_data.get('fake_price')
        description = cleaned_data.get('description')

        # Check if price is less than offer_price
        if price is not None and price is not None and fake_price < price:
            self.add_error('price', 'The price cannot be less than the offer price.')
            
        if description is not None and len(description) > 500:
            self.add_error('description', 'The description cannot be more than 500 characters.')

        return cleaned_data

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product' , 'order_quantity']
        