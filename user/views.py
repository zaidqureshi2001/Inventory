from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product , Order ,Profile
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout ,login as auth_login
from .forms import CreateUserForm , UserUpdateForm , ProfileUpdateForm , ProductForm , OrderForm
from django.contrib.auth.decorators import login_required
from django.views import View
import stripe
from django.conf import settings
from .models import User, ShippingAddress, Order, OrderItem, Product
import logging
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
import stripe
from .models import User, ShippingAddress, Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from django.http import JsonResponse
from datetime import datetime, timedelta
from collections import defaultdict
import json
from django.shortcuts import render
import json
from itertools import groupby
import json
from django.shortcuts import render, redirect
import stripe
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils import timezone



from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Save the form and create a user
            user = form.save()
            username = form.cleaned_data.get('username')

            # Prepare the email content
            subject = 'Welcome to Our Platform!'
            from_email = settings.EMAIL_HOST_USER  # The email you set in settings.py
            recipient_list = [user.email]  # The email provided by the user during registration

            # HTML email content
            message = f"""
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Welcome Email</title>
                <style>
                  body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f7f6;
                  }}
                  .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                  }}
                  .email-header {{
                    background-color: #007bff;
                    color: #ffffff;
                    padding: 30px 20px;
                    text-align: center;
                    font-size: 28px;
                    font-weight: bold;
                  }}
                  .email-body {{
                    padding: 40px 30px;
                    color: #333;
                    line-height: 1.6;
                  }}
                  .email-body h2 {{
                    color: #007bff;
                    font-size: 24px;
                    margin-bottom: 20px;
                  }}
                  .cta-btn {{
                    display: inline-block;
                    background-color: #28a745;
                    color: #ffffff;
                    font-size: 18px;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    text-align: center;
                    margin-top: 20px;
                    transition: background-color 0.3s ease;
                  }}
                  .cta-btn:hover {{
                    background-color: #218838;
                  }}
                  .footer {{
                    background-color: #f9f9f9;
                    color: #777;
                    padding: 20px;
                    text-align: center;
                    font-size: 14px;
                    border-top: 1px solid #ddd;
                  }}
                  .footer a {{
                    color: #007bff;
                    text-decoration: none;
                  }}
                  .footer a:hover {{
                    text-decoration: underline;
                  }}
                  .social-icons {{
                    margin-top: 15px;
                  }}
                  .social-icons a {{
                    color: #007bff;
                    font-size: 20px;
                    margin: 0 15px;
                    text-decoration: none;
                  }}
                </style>
              </head>
              <body>
                <div class="email-container">
                  <!-- Header Section -->
                  <div class="email-header">
                    Welcome to Our Platform, {username}
                  </div>

                  <!-- Body Section -->
                  <div class="email-body">
                    <h2>Hello {username},</h2>
                    <p>We are thrilled to have you as a member of our community! Thank you for signing up. To get started, we've got some exciting things waiting for you:</p>
                    
                    <p>Enjoy exclusive discounts and browse through a wide range of products on our platform.</p>
                    
                    <p>Click below to start your journey:</p>
                    
                    <a href="http://yourwebsite.com" class="cta-btn" target="_blank">Start Shopping Now</a>
                    
                    <div class="social-icons">
                      <p>Follow us on social media for the latest updates:</p>
                      <a href="https://facebook.com" target="_blank">Facebook</a>
                      <a href="https://twitter.com" target="_blank">Twitter</a>
                      <a href="https://instagram.com" target="_blank">Instagram</a>
                    </div>
                  </div>

                  <!-- Footer Section -->
                  <div class="footer">
                    <p>Need help? <a href="http://yourwebsite.com/help" target="_blank">Visit our help center</a>.</p>
                    <p>Thank you for joining our community! We're excited to have you.</p>
                    <p>&copy; 2025 Your Platform, All rights reserved.</p>
                  </div>
                </div>
              </body>
            </html>
            """

            # Send the email
            send_mail(subject, message, from_email, recipient_list, html_message=message)

            # Display success message and redirect to login page
            messages.success(request, f"Account successfully created for {username}!")
            return redirect('login')  
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'dashboard/register.html', context)






def login(request):
    if request.method == 'POST':
        username = request.POST.get("username") 
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request , user)
            return redirect('test')
        else:
            messages.error(request , 'Username OR Password Is Incorrect')
            

    return render(request , 'dashboard/login.html')

def user_logout(request):
    logout(request  )
    return redirect('login')



def test(request):
    cart = request.session.get('cart', {})
    print("cart_length", len(cart))

    # Initialize default values for anonymous users
    orders = Order.objects.none()  # No orders for anonymous users
    order_chart = Order.objects.all()
    order_items = OrderItem.objects.select_related('order').all()  # Fetch OrderItem objects
    product = Product.objects.all()[:12]
    workers = User.objects.all()
    worker = workers.count()
    order_count = Order.objects.count()
    successful_orders = Order.objects.filter(payment_status='success')
    product_count = Product.objects.count()
    items = Product.objects.filter(quantity__lt=50)
    lowstock_count = items.count()
    order_data = defaultdict(int)

    # Fetch new arrival products
    new_arrivals = Product.objects.filter(new_arrival=True)

    # If the user is authenticated, filter orders by the current user
    if request.user.is_authenticated:
        orders = Order.objects.filter(staff=request.user)  # Only for logged-in users

    # Group OrderItems by the date their associated order was created
    for order_item in order_items:
        created_at = order_item.order.created_at  # Use the order's created_at field
        if created_at:
            date_str = created_at.date()  # Use the date part for aggregation
            order_data[date_str] += 1  # Increment count for each OrderItem
    order_dates = sorted(order_data.keys())
    order_quantities = [order_data[date] for date in order_dates]

    context = {
        'cart_items': cart,
        'Lowstock_count': lowstock_count,
        'order': orders,  # Orders for the logged-in user (empty for anonymous)
        'product': product,
        'order_chart': order_chart,
        'workers': workers,
        'worker': worker,
        'order_count': order_count,
        'orders': successful_orders,
        'product_count': product_count,
        'order_dates': order_dates,
        'order_quantities': order_quantities,  # Pass the order counts to the template
        'new_arrivals': new_arrivals,  # Pass the new_arrivals to the template
    }

    return render(request, 'test.html', context)


@login_required(login_url='login')
def staff(request):
    items = Product.objects.filter(quantity__lt=50)
    Lowstock_count =items.count()
    xyz = Product.objects.all()
    workers = User.objects.all()
    worker = workers.count()
    order_count = Order.objects.count()
    orders = Order.objects.filter(payment_status='success')
    product_count = Product.objects.count()
    context = {
        'Lowstock_count':Lowstock_count ,
        'workers':workers,
        'worker':worker,
        'xyz' : xyz,
        'order_count' : order_count,
        'orders': orders,
        'product_count':product_count
    }
    return render(request , 'dashboard/staff.html' , context)

@login_required(login_url='login')
def top(request):
    return render(request , 'partials/top.html')

@login_required(login_url='login')
def product(request):
    items = Product.objects.filter(quantity__lt=50)
    Lowstock_count =items.count()
    items = Product.objects.all()
    product_count = Product.objects.count()
    workers = User.objects.all()
    worker = workers.count()
    order_count = Order.objects.count()
    orders = Order.objects.filter(payment_status='success')
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            prdct = form.cleaned_data.get('name')
            messages.success(request, f"{prdct}" + 'has been added ')
            return redirect('product')
    else:
        form = ProductForm()
     
    context  = {
        'Lowstock_count':Lowstock_count,
        'items': items ,
        'form' : form  ,
        'product_count':product_count,
        'order_count' : order_count,
        'orders': orders,
        'worker':worker
    }
    return render(request , 'dashboard/product.html', context)

@login_required(login_url='login')
def order(request):
    items = Product.objects.filter(quantity__lt=50)
    Lowstock_count =items.count()
    order_count = Order.objects.count()
    orders = Order.objects.filter(payment_status='success')
    workers = User.objects.all()
    worker = workers.count()
    product_count = Product.objects.count()
    orders_with_subtotals = []
    for order in orders:
        print(order)
        subtotal = sum(
            item.product.price * item.quantity for item in order.orderitem_set.all()
        )
        orders_with_subtotals.append({
            'order': order,
            'subtotal': subtotal,
        })
    context = {
        'orders_with_subtotals': orders_with_subtotals,
        'Lowstock_count':Lowstock_count ,
        'order_count' : order_count,
        'orders': orders,
        'worker':worker,
        'product_count':product_count
    }
    return render(request , 'dashboard/order.html' , context)


@login_required(login_url='login')
def profile(request):
    cart = request.session.get('cart', {})
    context={
        'hide_top': True,
        'cart_items':cart,
    }
    return render(request , 'dashboard/profile.html' , context)


@login_required(login_url='login')
def profile_update(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST , instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'cart_items':cart,
        'user_form' : user_form,
        'profile_form':profile_form,
        }
    return render(request , 'dashboard/profile_update.html', context)

@login_required(login_url='login')
def delete(request , pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('product')
    return render(request , 'dashboard/delete.html')

@login_required(login_url='login')
def product_update(request , pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST , instance=item)
        if form.is_valid():
            form.save()
            return redirect('product')            
    else:
        form = ProductForm(instance=item)

    context = {
        'form' : form
    }
    return render (request , 'dashboard/product_update.html' , context)

@login_required(login_url='login')
def staff_details(request , pk):
    workers =User.objects.get(id=pk)
    context ={
        'hide_top': True,
        'workers':workers
    }
    return render(request  , 'dashboard/staff_details.html' , context)

@login_required(login_url='login')
def Lowstock(request):
    items = Product.objects.filter(quantity__lt=50)
    Lowstock_count =items.count()
    product = Product.objects.all()
    workers = User.objects.all()
    worker = workers.count()
    order_count = Order.objects.count()
    orders = Order.objects.filter(payment_status='success')
    product_count = Product.objects.count()
    context = {
    'Lowstock_count': Lowstock_count,
    'items':items,
    'order':order,
    'product':product ,
    'workers':workers,
    'worker':worker,
    'order_count' : order_count,
    'orders': orders,
    'product_count':product_count
    }
    return render(request , 'dashboard/Lowstock.html' ,context)


##############################################################################
from django.shortcuts import get_object_or_404

# @login_required(login_url='login')
def addto_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    quantity_in_cart = cart.get(str(product_id), {}).get('quantity', 0)
    if quantity_in_cart < product.quantity:
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'product_id': product.id,  
                'name': product.name,
                'price': str(product.price),
                'quantity': 1,
                'description': product.description,
                'image': product.image.url
            }

        # Debugging: Print the cart structure before saving
        print("Cart after adding item:", cart)
        request.session['cart'] = cart
        print("Cart length:", len(cart))
        messages.success(request, f'{product.name} has been added to cart')
    else:
        messages.error(request, f'Not enough stock available for {product.name}')
    return redirect('test')  

def cart(request):
    cart = request.session.get('cart', {})
    total_price = 0
    for item in cart.values():
        if 'product_id' not in item:
            print(f"Missing 'product_id' in cart item: {item}")
            continue

        item['total_price'] = float(item['price']) * item['quantity']
        total_price += item['total_price']

        try:
            product = Product.objects.get(id=item['product_id'])
            item['available_stock'] = product.quantity  # Add available stock to the cart item
        except Product.DoesNotExist:
            item['available_stock'] = 0  # If the product is missing, set stock to 0

    context = {'cart_items': cart, 'total_price': total_price}
    return render(request, 'dashboard/cart.html', context)

# View to update cart quantity (increase or decrease)
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

# View to update cart quantity (increase or decrease)
def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    try:
        # Get the product from the database
        product = Product.objects.get(id=product_id)
        available_stock = product.quantity  # Get the available stock for the product
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found.'})
    
    if str(product_id) in cart:
        current_quantity = cart[str(product_id)]['quantity']
        
        if action == 'increase':
            if current_quantity >= available_stock:
                return JsonResponse({'success': False, 'error': 'Cannot increase quantity above available stock.'})
            cart[str(product_id)]['quantity'] += 1
        
        elif action == 'decrease' and current_quantity > 1:
            cart[str(product_id)]['quantity'] -= 1
        
        # Recalculate total price
        total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
        
        request.session['cart'] = cart
        return JsonResponse({
            'success': True,
            'new_quantity': cart[str(product_id)]['quantity'],
            'new_total_price': total_price
        })
    
    return JsonResponse({'success': False})

# View to remove an item from the cart
def delete_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        
        # Recalculate total price
        total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
        
        # Prepare updated cart items HTML to send back
        cart_items = cart.items()  # Get all cart items
        cart_html = render(request, 'cart_items.html', {'cart_items': cart_items, 'total_price': total_price}).content.decode('utf-8')
        
        request.session['cart'] = cart
        return JsonResponse({
            'success': True,
            'new_total_price': total_price,
            'cart_html': cart_html  # Send updated cart HTML
        })
    
    return JsonResponse({'success': False})

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    user = request.user
    saved_cards = []  # Fetch saved cards from the user's Stripe profile
    if user.profile.stripe_customer_id:
        saved_cards = stripe.PaymentMethod.list(customer=user.profile.stripe_customer_id, type='card')
        print(saved_cards)

    if not cart:
        return redirect('cart')  # Redirect to cart if there are no items

    # Remove duplicate cards based on their `last4`
    unique_cards = {}
    for card in saved_cards:
        last4 = card.card.last4
        if last4 not in unique_cards:
            unique_cards[last4] = card

    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())

    # Get unique previous addresses
    previous_address = ShippingAddress.objects.filter(customer=request.user)
    unique_addresses = list({address.address: address for address in previous_address}.values())

    # Serialize previous addresses for JSON usage
    previous_address_json = json.dumps([{
        'id': address.id,
        'address': address.address,
        'city': address.city,
        'state': address.state,
        'zipcode': address.zipcode,
        'phone_no': address.phone_no,
    } for address in unique_addresses])
    
    return render(request, 'dashboard/checkout.html', {
        'saved_cards': unique_cards.values(),  # Pass unique cards
        'cart_items': cart,
        'total_price': total_price,
        'previous_address_json': previous_address_json,
        'previous_address': unique_addresses,
    })


def delete_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]  
    request.session['cart'] = cart

    total_price = 0
    for item in cart.values():
        total_price += float(item['price']) * item['quantity']

    return JsonResponse({
        'success': True,
        'new_total_price': total_price
    })



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def myorder(request):
    # Fetch only the orders related to the logged-in user
    orders = Order.objects.filter(staff=request.user).prefetch_related('orderitem_set').order_by('-date')  # Adjust relationship name if different
    cart = request.session.get('cart', {})
    orders_with_subtotals = []
    for order in orders:
        subtotal = sum(
            item.product.price * item.quantity for item in order.orderitem_set.all()
        )
        orders_with_subtotals.append({
            'order': order,
            'subtotal': subtotal,
        })
    context = {
        'cart_items':cart,
        'orders': orders,
        'orders_with_subtotals': orders_with_subtotals,
    }
    return render(request, 'dashboard/my_order.html', context)

#*******************************************

logger = logging.getLogger(__name__)


import stripe
import logging
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .models import ShippingAddress, Product, User
from django.urls import reverse

# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Logger for debugging purposes
logger = logging.getLogger(__name__)

import stripe
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from .models import User, ShippingAddress, Product, Order, OrderItem



from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
import stripe
from django.utils import timezone
from .models import User, Order, OrderItem, ShippingAddress, Product
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
import stripe


from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class ProcessCheckoutView(View):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        phone_no = request.POST.get('phone_no')
        selected_card = request.POST.get('saved_card')

        # Ensure user exists
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.email}")
        except User.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'User not found'}, status=404)

        # Fetch or create Stripe customer ID
        user_profile = user.profile
        stripe_customer_id = user_profile.stripe_customer_id

        if not stripe_customer_id:
            # Create a new customer in Stripe if one doesn't exist
            stripe_customer = stripe.Customer.create(email=email)
            user_profile.stripe_customer_id = stripe_customer.id
            user_profile.save()
            stripe_customer_id = stripe_customer.id
            print(f"New Stripe customer created: {stripe_customer.id}")

        # Create a shipping address
        shipping_address = ShippingAddress.objects.create(
            customer=user,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            phone_no=phone_no,
        )
        print(f"Shipping address created for {user.email} at {shipping_address.address}")

        # Calculate the total price of the cart
        total_price = 0
        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({'status': 'failed', 'message': 'Cart is empty or missing'}, status=400)

        product_details = []  # To store product name, quantity, and price for the email
        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                total_price += product.price * item['quantity']
                product_details.append(f"{product.name} - Quantity: {item['quantity']} @ ₹{product.price} each")
                print(f"Product: {product.name}, Quantity: {item['quantity']}, Price: {product.price}")
            except Product.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

        print(f"Total cart price: {total_price}")
        
        # Handle payment with a saved card
        if selected_card and selected_card != "new":
            try:
                # Create PaymentIntent with the saved card
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(total_price * 100),  # Convert price to cents
                    currency='INR',
                    customer=stripe_customer_id,
                    payment_method=selected_card,
                    off_session=True,
                    confirm=True,
                )
                payment_intent_id = payment_intent.id
                print(f"PaymentIntent created: {payment_intent_id}")

                # Handle payment status
                print(f"PaymentIntent status: {payment_intent.status}")

                if payment_intent.status == 'requires_action' or payment_intent.status == 'requires_source_action':
                    return JsonResponse({
                        'status': 'requires_action',
                        'message': 'Action required for payment confirmation.',
                        'payment_intent_client_secret': payment_intent.client_secret
                    })
                elif payment_intent.status == 'succeeded':
                    print('Payment is successful')

                    # Create the order
                    order = Order.objects.create(
                        staff=user,
                        date=timezone.now(),
                        payment_status='success',
                        shipping_address=shipping_address
                    )
                    
                    total_price = 0
                    for product_id, item in cart.items():
                        try:
                            product = Product.objects.get(id=product_id)
                            total_price += product.price * item['quantity']

                            # Create order item
                            OrderItem.objects.create(
                                product=product,
                                quantity=item['quantity'],
                                order=order
                            )

                            # Check stock availability
                            if product.quantity < item['quantity']:
                                return JsonResponse({'status': 'failed', 'message': f'Not enough stock for product {product.name}'}, status=400)

                            # Deduct stock
                            product.quantity -= item['quantity']
                            product.save()

                        except Product.DoesNotExist:
                            return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

                    # Update order total price and save
                    order.total_price = total_price
                    order.save()

                    # Send order confirmation email
                    html_content = f"""
                    <html>
                    <head>
                        <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            background-color: #f4f4f4;
                            color: #333;
                            margin: 0;
                            padding: 0;
                            word-wrap: break-word;
                        }}
                        .email-container {{
                            width: 100%;
                            max-width: 800px;
                            margin: 0 auto;
                            background-color: #ffffff;
                            border-radius: 8px;
                            padding: 20px;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        }}
                        .email-header {{
                            background-color: #007bff;
                            color: #ffffff;
                            padding: 30px 20px;
                            text-align: center;
                            font-size: 28px;
                            font-weight: bold;
                        }}
                        .email-body {{
                            padding: 40px 30px;
                            color: #333;
                            line-height: 1.6;
                        }}
                        .email-body h2 {{
                            color: #007bff;
                            font-size: 24px;
                            margin-bottom: 20px;
                        }}
                        .cta-btn {{
                            display: inline-block;
                            background-color: #28a745;
                            color: #ffffff;
                            font-size: 18px;
                            padding: 15px 30px;
                            text-decoration: none;
                            border-radius: 5px;
                            text-align: center;
                            margin-top: 20px;
                            transition: background-color 0.3s ease;
                        }}
                        .cta-btn:hover {{
                            background-color: #218838;
                        }}
                        .footer {{
                            background-color: #f9f9f9;
                            color: #777;
                            padding: 20px;
                            text-align: center;
                            font-size: 14px;
                            border-top: 1px solid #ddd;
                        }}
                        .footer a {{
                            color: #007bff;
                            text-decoration: none;
                        }}
                        .footer a:hover {{
                            text-decoration: underline;
                        }}
                        .order-summary-table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                            table-layout: fixed;
                        }}
                        .order-summary-table th, .order-summary-table td {{
                            padding: 8px;
                            border: 1px solid #ddd;
                            text-align: left;
                            word-wrap: break-word;
                        }}
                        .order-summary-table th {{
                            background-color: #f2f2f2;
                        }}
                        .order-summary-table td.right {{
                            text-align: right;
                        }}
                        .shipping-address {{
                            background-color: #f8f8f8;
                            padding: 20px;
                            border-radius: 8px;
                            margin-top: 20px;
                        }}
                        .shipping-address h3 {{
                            font-size: 22px;
                            color: #333;
                            margin-bottom: 10px;
                        }}
                        .product-image {{
                            width: 50px;
                            height: auto;
                            margin-right: 10px;
                            vertical-align: middle;
                        }}
                        .payment-summary-table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                            font-size: 14px;
                        }}
                        .payment-summary-table th, .payment-summary-table td {{
                            padding: 6px;
                            border: 1px solid #ddd;
                            text-align: left;
                        }}
                        .payment-summary-table td.right {{
                            text-align: right;
                        }}
                        </style>
                    </head>
                    <body>
                        <div class="email-container">
                        <!-- Header Section -->
                        <div class="email-header">
                            Order Confirmation - Order ID: {order.id}
                        </div>

                        <!-- Body Section -->
                        <div class="email-body">
                            <h2>Thank you for your order, {user.username}!</h2>
                            <p>We have received your order and are processing it now. Below are the details of your order:</p>

                            <!-- Shipping Details -->
                            <div class="shipping-address">
                            <h3>Delivery Address:</h3>
                            <p><strong>{shipping_address.address}</strong></p>
                            <p>{shipping_address.city}, {shipping_address.state} - {shipping_address.zipcode}</p>
                            <p>Phone: {shipping_address.phone_no}</p>
                            </div>

                            <!-- Order Summary -->
                            <h3 style="text-align: center; font-size: 22px; color: #333;">Order Summary</h3>
                            <table class="order-summary-table">
                            <thead>
                                <tr>
                                <th>Product</th>
                                <th>Details</th>
                                <th>Price</th>
                                </tr>
                            </thead>
                            <tbody>
                    """

                    # Initialize subtotal
                    subtotal = 0

                    # Add product list dynamically
                    for product_id, item in cart.items():
                        try:
                            product = Product.objects.get(id=product_id)
                            total_product_price = product.price * item['quantity']
                            image_url = request.build_absolute_uri(product.image.url)
                            subtotal += total_product_price
                            html_content += f"""
                            <tr>
                            <td>
                                <img src="{image_url}" alt="{product.name}" class="product-image">
                                {product.name}
                            </td>
                            <td>Quantity: {item['quantity']}</td>
                            <td class="right">₹{total_product_price}</td>
                            </tr>
                            """
                        except Product.DoesNotExist:
                            continue

                    # Assuming there's a shipping fee or taxes, for example
                    shipping_fee = 50  # Placeholder for shipping fee
                    total_price = subtotal + shipping_fee

                    html_content += f"""
                            </tbody>
                            </table>

                            <!-- Payment Summary Table -->
                            <h3 style="text-align: center; font-size: 18px; color: #333; margin-top: 30px;">Payment Summary</h3>
                            <table class="payment-summary-table">
                            <tbody>
                                <tr>
                                <td style="font-weight: bold;">Subtotal</td>
                                <td class="right">₹{subtotal}</td>
                                </tr>
                                <tr>
                                <td style="font-weight: bold;">Shipping</td>
                                <td class="right">₹{shipping_fee}</td>
                                </tr>
                                <tr style="border-top: 1px solid #ddd;">
                                <td style="font-weight: bold;">Total</td>
                                <td class="right">₹{total_price}</td>
                                </tr>
                            </tbody>
                            </table>

                            <!-- Customer Support Section -->
                            <div style="background-color: #f8f8f8; padding: 20px; margin-top: 20px; text-align: center;">
                            <p>If you have any queries, please contact us at:</p>
                            <p>Email: <a href="mailto:xyz@example.com" style="color: #333; text-decoration: none;">xyz@example.com</a><br>
                                Customer Care No: +123-456-7890</p>
                            </div>

                            <!-- Closing Remarks -->
                            <div style="text-align: center; margin-top: 20px; font-size: 16px; color: #555;">
                            <p>We look forward to your next order! Stay connected with us.</p>
                            <p>Thank you for shopping with us!</p>
                            <a href="http://yourwebsite.com" target="_blank" class="cta-btn">Visit Our Website</a>
                            </div>
                        </div>

                        <!-- Footer Section -->
                        <div class="footer">
                            <p>&copy; 2025 Your Platform, All rights reserved.</p>
                            <p><a href="http://yourwebsite.com/help" target="_blank">Need Help? Visit our help center</a></p>
                        </div>
                        </div>
                    </body>
                    </html>
                    """

                    # Plain text version of the email (fallback)
                    text_content = f"""
                    Dear {user.first_name} {user.last_name},

                    Thank you for your order! Your order {order.id} has been successfully placed.

                    Shipping Address:
                    {shipping_address.address}
                    {shipping_address.city}, {shipping_address.state} - {shipping_address.zipcode}
                    Phone: {shipping_address.phone_no}

                    Order Details:
                    """

                    for product_id, item in cart.items():
                        try:
                            product = Product.objects.get(id=product_id)
                            total_product_price = product.price * item['quantity']
                            text_content += f"{product.name} - Quantity: {item['quantity']} @ ₹{product.price} Total: ₹{total_product_price}\n"
                        except Product.DoesNotExist:
                            continue

                    text_content += f"""
                    Subtotal: ₹{subtotal}
                    Shipping: ₹{shipping_fee}
                    Total: ₹{total_price}

                    If you have any queries, please contact us at:
                    Email: xyz@example.com
                    Customer Care No: +123-456-7890

                    We look forward to your next order! Stay connected with us.

                    Thank you for shopping with us!
                    """

                    # Send the email with both plain text and HTML
                    email_subject = f"Order Confirmation - {order.id}"
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [user.email]

                    msg = EmailMultiAlternatives(
                        email_subject, 
                        text_content, 
                        from_email, 
                        recipient_list
                    )
                    msg.attach_alternative(html_content, "text/html")

                    # Send the email
                    try:
                        msg.send()
                        print(f"Order confirmation email sent to {user.email}")
                    except Exception as e:
                        print(f"Error sending email: {str(e)}")





                    # Clear the cart in the session
                    if 'cart' in request.session:
                        del request.session['cart']
                        request.session.modified = True

                    # Redirect to success page
                    return redirect(reverse('success'))

                else:
                    return JsonResponse({'status': 'failed', 'message': 'Payment failed'}, status=400)

            except stripe.error.CardError as e:
                return JsonResponse({'status': 'failed', 'message': e.user_message}, status=400)
            except stripe.error.StripeError as e:
                return JsonResponse({'status': 'failed', 'message': 'An error occurred during payment processing.'}, status=500)
            except Exception as e:
                return JsonResponse({'status': 'failed', 'message': 'An unexpected error occurred'}, status=500)

        # Handle creation of Stripe session if the card is new
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {'name': f'Order for {email}'},  # Order name as email or user
                        'unit_amount': int(total_price * 100),  # Convert price to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                metadata={
                    'user_id': user.id,
                    'shipping_address_id': shipping_address.id,
                    'cart_data': str(cart),  # Convert cart data into string for metadata
                },
                shipping_address_collection={
                    'allowed_countries': ['IN'],
                },
                customer=stripe_customer_id,
                success_url=request.build_absolute_uri('/success'),
                cancel_url=request.build_absolute_uri('/cancel'),
            )

            # Clear the cart in the session
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True

            # Redirect to the checkout session
            return redirect(checkout_session.url, code=303)
        
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': 'Payment session creation failed'}, status=500)


import json
import stripe
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .models import Order, ShippingAddress, OrderItem, Product
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.http import JsonResponse
from .models import User, ShippingAddress, Product, Order, OrderItem
import stripe
from datetime import timezone


from django.utils import timezone
from .models import User, ShippingAddress, Product, Order, OrderItem


@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        try:
            # Verify Stripe signature
            event = stripe.Webhook.construct_event(
                payload, request.headers.get('Stripe-Signature'), endpoint_secret
            )
        except ValueError as e:
            print(f"Invalid payload: {str(e)}")
            return JsonResponse({'status': 'failed', 'message': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            print(f"Invalid signature: {str(e)}")
            return JsonResponse({'status': 'failed', 'message': 'Invalid signature'}, status=400)

        # Handle Stripe event
        event_type = event.get('type')
        event_data = event['data']['object']

        if event_type == 'checkout.session.completed':
            print("Checkout session completed event received")
            session_id = event_data.get('id')
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Extract metadata
            metadata = session.get('metadata', {})
            user_id = metadata.get('user_id')
            shipping_address_id = metadata.get('shipping_address_id')
            cart_data = metadata.get('cart_data')

            if not user_id or not shipping_address_id or not cart_data:
                print("Missing necessary metadata fields (user_id, shipping_address_id, or cart_data)")
                return JsonResponse({'status': 'failed', 'message': 'Missing metadata fields'}, status=400)

            try:
                user = User.objects.get(id=user_id)
                shipping_address = ShippingAddress.objects.get(id=shipping_address_id)
                cart = eval(cart_data)  # Rebuild cart data from string
                print(f"Cart data: {cart}")
            except Exception as e:
                print(f"Error retrieving user or shipping address: {str(e)}")
                return JsonResponse({'status': 'failed', 'message': 'Error retrieving user data'}, status=500)

            # Check the payment intent status
            payment_intent_id = session.get('payment_intent')
            try:
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            except stripe.error.StripeError as e:
                print(f"Error retrieving payment intent: {str(e)}")
                return JsonResponse({'status': 'failed', 'message': 'Error retrieving payment intent'}, status=500)

            print(f"Payment intent status: {payment_intent.status}")

            if payment_intent.status == 'succeeded':
                # Create the order after successful payment
                order = Order.objects.create(
                    staff=user,
                    date=timezone.now(),  # Corrected usage of timezone.now()
                    payment_status='success',
                    shipping_address=shipping_address
                )

                total_price = 0
                product_details = []  # To store product details for the email
                for product_id, item in cart.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        total_price += product.price * item['quantity']

                        # Create order item
                        OrderItem.objects.create(
                            product=product,
                            quantity=item['quantity'],
                            order=order
                        )

                        # Check stock availability
                        if product.quantity < item['quantity']:
                            print(f"Not enough stock for product {product.name}")
                            return JsonResponse({'status': 'failed', 'message': f'Not enough stock for product {product.name}'}, status=400)

                        # Deduct stock
                        product.quantity -= item['quantity']
                        product.save()

                    except Product.DoesNotExist:
                        print(f"Product with ID {product_id} does not exist")
                        return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

                # Update order total price and save
                order.total_price = total_price
                order.save()

                # Send confirmation email and other actions here...
                html_content = f"""
                <html>
                <head>
                    <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        background-color: #f4f4f4;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        word-wrap: break-word;
                    }}
                    .email-container {{
                        width: 100%;
                        max-width: 800px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        border-radius: 8px;
                        padding: 20px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    }}
                    .email-header {{
                        background-color: #007bff;
                        color: #ffffff;
                        padding: 30px 20px;
                        text-align: center;
                        font-size: 28px;
                        font-weight: bold;
                    }}
                    .email-body {{
                        padding: 40px 30px;
                        color: #333;
                        line-height: 1.6;
                    }}
                    .email-body h2 {{
                        color: #007bff;
                        font-size: 24px;
                        margin-bottom: 20px;
                    }}
                    .cta-btn {{
                        display: inline-block;
                        background-color: #28a745;
                        color: #ffffff;
                        font-size: 18px;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 5px;
                        text-align: center;
                        margin-top: 20px;
                        transition: background-color 0.3s ease;
                    }}
                    .cta-btn:hover {{
                        background-color: #218838;
                    }}
                    .footer {{
                        background-color: #f9f9f9;
                        color: #777;
                        padding: 20px;
                        text-align: center;
                        font-size: 14px;
                        border-top: 1px solid #ddd;
                    }}
                    .footer a {{
                        color: #007bff;
                        text-decoration: none;
                    }}
                    .footer a:hover {{
                        text-decoration: underline;
                    }}
                    .order-summary-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                        table-layout: fixed;
                    }}
                    .order-summary-table th, .order-summary-table td {{
                        padding: 8px;
                        border: 1px solid #ddd;
                        text-align: left;
                        word-wrap: break-word;
                    }}
                    .order-summary-table th {{
                        background-color: #f2f2f2;
                    }}
                    .order-summary-table td.right {{
                        text-align: right;
                    }}
                    .shipping-address {{
                        background-color: #f8f8f8;
                        padding: 20px;
                        border-radius: 8px;
                        margin-top: 20px;
                    }}
                    .shipping-address h3 {{
                        font-size: 22px;
                        color: #333;
                        margin-bottom: 10px;
                    }}
                    .product-image {{
                        width: 50px;
                        height: auto;
                        margin-right: 10px;
                        vertical-align: middle;
                    }}
                    .payment-summary-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                        font-size: 14px;
                    }}
                    .payment-summary-table th, .payment-summary-table td {{
                        padding: 6px;
                        border: 1px solid #ddd;
                        text-align: left;
                    }}
                    .payment-summary-table td.right {{
                        text-align: right;
                    }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                    <!-- Header Section -->
                    <div class="email-header">
                        Order Confirmation - Order ID: {order.id}
                    </div>

                    <!-- Body Section -->
                    <div class="email-body">
                        <h2>Thank you for your order, {user.username}!</h2>
                        <p>We have received your order and are processing it now. Below are the details of your order:</p>

                        <!-- Shipping Details -->
                        <div class="shipping-address">
                        <h3>Delivery Address:</h3>
                        <p><strong>{shipping_address.address}</strong></p>
                        <p>{shipping_address.city}, {shipping_address.state} - {shipping_address.zipcode}</p>
                        <p>Phone: {shipping_address.phone_no}</p>
                        </div>

                        <!-- Order Summary -->
                        <h3 style="text-align: center; font-size: 22px; color: #333;">Order Summary</h3>
                        <table class="order-summary-table">
                        <thead>
                            <tr>
                            <th>Product</th>
                            <th>Details</th>
                            <th>Price</th>
                            </tr>
                        </thead>
                        <tbody>
                """

                # Initialize subtotal
                subtotal = 0

                # Add product list dynamically
                for product_id, item in cart.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        total_product_price = product.price * item['quantity']
                        image_url = request.build_absolute_uri(product.image.url)
                        subtotal += total_product_price
                        html_content += f"""
                        <tr>
                        <td>
                            <img src="{image_url}" alt="{product.name}" class="product-image">
                            {product.name}
                        </td>
                        <td>Quantity: {item['quantity']}</td>
                        <td class="right">₹{total_product_price}</td>
                        </tr>
                        """
                    except Product.DoesNotExist:
                        continue

                # Assuming there's a shipping fee or taxes, for example
                shipping_fee = 50  # Placeholder for shipping fee
                total_price = subtotal + shipping_fee

                html_content += f"""
                        </tbody>
                        </table>

                        <!-- Payment Summary Table -->
                        <h3 style="text-align: center; font-size: 18px; color: #333; margin-top: 30px;">Payment Summary</h3>
                        <table class="payment-summary-table">
                        <tbody>
                            <tr>
                            <td style="font-weight: bold;">Subtotal</td>
                            <td class="right">₹{subtotal}</td>
                            </tr>
                            <tr>
                            <td style="font-weight: bold;">Shipping</td>
                            <td class="right">₹{shipping_fee}</td>
                            </tr>
                            <tr style="border-top: 1px solid #ddd;">
                            <td style="font-weight: bold;">Total</td>
                            <td class="right">₹{total_price}</td>
                            </tr>
                        </tbody>
                        </table>

                        <!-- Customer Support Section -->
                        <div style="background-color: #f8f8f8; padding: 20px; margin-top: 20px; text-align: center;">
                        <p>If you have any queries, please contact us at:</p>
                        <p>Email: <a href="mailto:xyz@example.com" style="color: #333; text-decoration: none;">xyz@example.com</a><br>
                            Customer Care No: +123-456-7890</p>
                        </div>

                        <!-- Closing Remarks -->
                        <div style="text-align: center; margin-top: 20px; font-size: 16px; color: #555;">
                        <p>We look forward to your next order! Stay connected with us.</p>
                        <p>Thank you for shopping with us!</p>
                        <a href="http://yourwebsite.com" target="_blank" class="cta-btn">Visit Our Website</a>
                        </div>
                    </div>

                    <!-- Footer Section -->
                    <div class="footer">
                        <p>&copy; 2025 Your Platform, All rights reserved.</p>
                        <p><a href="http://yourwebsite.com/help" target="_blank">Need Help? Visit our help center</a></p>
                    </div>
                    </div>
                </body>
                </html>
                """

                # Plain text version of the email (fallback)
                text_content = f"""
                Dear {user.first_name} {user.last_name},

                Thank you for your order! Your order {order.id} has been successfully placed.

                Shipping Address:
                {shipping_address.address}
                {shipping_address.city}, {shipping_address.state} - {shipping_address.zipcode}
                Phone: {shipping_address.phone_no}

                Order Details:
                """

                for product_id, item in cart.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        total_product_price = product.price * item['quantity']
                        text_content += f"{product.name} - Quantity: {item['quantity']} @ ₹{product.price} Total: ₹{total_product_price}\n"
                    except Product.DoesNotExist:
                        continue

                text_content += f"""
                Subtotal: ₹{subtotal}
                Shipping: ₹{shipping_fee}
                Total: ₹{total_price}

                If you have any queries, please contact us at:
                Email: xyz@example.com
                Customer Care No: +123-456-7890

                We look forward to your next order! Stay connected with us.

                Thank you for shopping with us!
                """

                # Send the email with both plain text and HTML
                email_subject = f"Order Confirmation - {order.id}"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]

                msg = EmailMultiAlternatives(
                    email_subject, 
                    text_content, 
                    from_email, 
                    recipient_list
                )
                msg.attach_alternative(html_content, "text/html")

                # Send the email
                try:
                    msg.send()
                    print(f"Order confirmation email sent to {user.email}")
                except Exception as e:
                    print(f"Error sending email: {str(e)}")


                    
                # Optionally clear the cart session here if needed
                if 'cart' in request.session:
                    print(f"Cart before clearing: {request.session['cart']}")
                    del request.session['cart']
                    request.session.save()  # Save the session after clearing the cart
                    request.session.modified = True
                    print("Cart cleared in webhook.")

                return JsonResponse({'status': 'success', 'message': 'Order created successfully'}, status=200)
            else:
                print(f"Payment failed with status {payment_intent.status}")
                return JsonResponse({'status': 'failed', 'message': 'Payment failed'}, status=400)

        # Handle other event types if needed
        return JsonResponse({'status': 'success', 'message': 'Event handled successfully'}, status=200)

    # If the request is not a POST request, return a method not allowed response
    return JsonResponse({'status': 'failed', 'message': 'Method not allowed'}, status=405)




def success(request):
    context = {
        'payment_status': 'success'
    }
    return render(request, 'dashboard/success.html', context)

def cancel(request):
    context = {
        'payment_status': 'cancel'
    }
    return render(request, 'dashboard/cancel.html', context)

def get_order_data(request):
    # Assuming you have the OrderItem model, which is related to an Order
    order_items = OrderItem.objects.select_related('order').all()
    order_data = defaultdict(int)

    # Aggregate orders by date
    for order_item in order_items:
        order_date = order_item.order.created_at.date()  # Ensure this is a date object
        order_data[order_date] += 1  # Increment by 1 for each order

    # Sort the dates and prepare the response
    order_dates = sorted(order_data.keys())
    order_counts = [order_data[date] for date in order_dates]

    # Return the data as JSON
    return JsonResponse({
        'dates': [date.strftime('%Y-%m-%d') for date in order_dates],  # Convert dates to string format
        'counts': order_counts
    })


# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, id):
    # Fetch the product by its ID, or return 404 if it doesn't exist
    product = get_object_or_404(Product, id=id)
    
    
    # Pass the product details to the template
    return render(request, 'dashboard/product_details.html', {'product': product})

