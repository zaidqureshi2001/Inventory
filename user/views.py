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

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save() 
            user = form.cleaned_data.get('username')
            messages.success(request, "Account is created for "+ user)
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
            messages.info(request , 'Username OR Password Is Incorrect')
            

    return render(request , 'dashboard/login.html')

def user_logout(request):
    logout(request  )
    return redirect('login')

@login_required(login_url='login')
# def test(request):
#     cart = request.session.get('cart', {})
#     print("cart_length" , len(cart))
#     order = Order.objects.filter(staff=request.user)
#     order_chart = Order.objects.all()
#     product = Product.objects.all()
#     workers = User.objects.all()
#     worker = workers.count()
#     order_count = Order.objects.count()
#     orders = Order.objects.filter(payment_status='success')
#     product_count = Product.objects.count()
#     items = Product.objects.filter(quantity__lt=50)
#     Lowstock_count =items.count()
#     context = {
#     'cart_items':cart,
#     'Lowstock_count':Lowstock_count,
#     'order':order,
#     'product':product ,
#     'order_chart':order_chart,
#     'workers':workers,
#     'worker':worker,
#     'order_count' : order_count,
#     'orders': orders,
#     'product_count':product_count
#     }
#     return render(request , 'test.html' , context)


@login_required(login_url='login')
def test(request):
    cart = request.session.get('cart', {})
    print("cart_length", len(cart))
    
    # Fetch orders and filter them as needed
    orders = Order.objects.filter(staff=request.user)
    order_chart = Order.objects.all()
    product = Product.objects.all()
    workers = User.objects.all()
    worker = workers.count()
    order_count = Order.objects.count()
    successful_orders = Order.objects.filter(payment_status='success')
    product_count = Product.objects.count()
    items = Product.objects.filter(quantity__lt=50)
    lowstock_count = items.count()
    order_data = defaultdict(int)

    # Group orders by the date they were created
    order_data= defaultdict(int)
    for order in order_chart:
        created_at = order.created_at
        if created_at:
            date_str = created_at.date()  # Use the date part for aggregation
            quantity = order.order_quantity if order.order_quantity else 0 
            print(f"Order created at: {created_at}, Date: {date_str}, Quantity: {quantity}")
            order_data[date_str] += order.order_quantity if order.order_quantity else 0
 # Aggregate the quantity for the day
    print("Aggregated order data:", order_data)


    # Sort the dates and order counts
    order_dates = [date.strftime("%Y-%m-%d") for date in order_data.keys()]
    order_quantities = list(order_data.values())
    print("Order Dates:", order_dates)
    print("Order Quantities:", order_quantities)

    context = {
        'cart_items': cart,
        'Lowstock_count': lowstock_count,
        'order': orders,
        'product': product,
        'order_chart': order_chart,
        'workers': workers,
        'worker': worker,
        'order_count': order_count,
        'orders': successful_orders,
        'product_count': product_count,
        'order_dates': order_dates,
        'order_quantities': order_quantities, # Pass the order counts to the template
    }

    return render(request, 'test.html', context)
from django.http import JsonResponse
from datetime import datetime, timedelta
from collections import defaultdict

def get_order_data(request):
    order_data = defaultdict(int)

    # Simulate order data
    for i in range(0, 7):  # Last 7 days
        date = datetime.now().date() - timedelta(days=i)
        order_data[date] = i * 5  # Example: 5, 10, 15, etc.

    # Format the data for JSON response
    response = {
        'dates': [date.strftime("%Y-%m-%d") for date in order_data.keys()],
        'quantities': list(order_data.values())
    }
    return JsonResponse(response)

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


def delete(request , pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('product')
    return render(request , 'dashboard/delete.html')

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

def staff_details(request , pk):
    workers =User.objects.get(id=pk)
    context ={
        'workers':workers
    }
    return render(request  , 'dashboard/staff_details.html' , context)


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

@login_required(login_url='login')
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
        
        total_price = 0
        for item in cart.values():
            total_price += float(item['price']) * item['quantity']

        request.session['cart'] = cart
        print(f"Cart after update: {cart}")
        return JsonResponse({
            'success': True,
            'new_quantity': cart[str(product_id)]['quantity'],
            'new_total_price': total_price
        })
    
    return JsonResponse({'success': False})

import json
from django.shortcuts import render
# def checkout(request):  
#     cart = request.session.get('cart', {})
#     if not cart:
#         return redirect('test')
#     total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
#     previous_address = ShippingAddress.objects.filter(customer=request.user)
#     print('hello' ,previous_address)
#     return render(request, 'dashboard/checkout.html', {
#         'cart_items': cart,
#         'total_price': total_price,
#         'previous_address': previous_address,
#     })
import json
from itertools import groupby

def checkout(request):
    cart = request.session.get('cart', {})
    user = request.user
    saved_cards = []  # Fetch saved cards from the user profile
    if user.profile.stripe_customer_id:
        saved_cards = stripe.PaymentMethod.list(customer=user.profile.stripe_customer_id, type='card')
    if not cart:
        return redirect('cart')  # Redirect to cart if no items
    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
    previous_address = ShippingAddress.objects.filter(customer=request.user)
    # Ensure unique addresses based on their content (e.g., address field)
    unique_addresses = list({address.address: address for address in previous_address}.values())
    # Serialize previous addresses to JSON format
    previous_address_json = json.dumps([{
        'id': address.id,
        'address': address.address,
        'city': address.city,
        'state': address.state,
        'zipcode': address.zipcode,
        'phone_no': address.phone_no,
    } for address in unique_addresses])
    
    return render(request, 'dashboard/checkout.html', {
        'saved_cards': saved_cards,
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


logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY
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

        try:
            # Ensure user exists
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'User not found'}, status=404)
        user_profile = user.profile
        if user_profile.stripe_customer_id:
            stripe_customer_id = user_profile.stripe_customer_id
        else:
            # Create a new customer in Stripe if not exists
            stripe_customer = stripe.Customer.create(email=email)
            # Save the customer ID in your database (e.g., in the User model)
            user_profile.stripe_customer_id = stripe_customer.id
            user_profile.save()
            stripe_customer_id = stripe_customer.id
        
        # Create shipping address
        shipping_address = ShippingAddress.objects.create(
            customer=user,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            phone_no=phone_no,
        )
        print(f"Stripe Customer ID: {stripe_customer_id}")  

        total_price = 0
        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({'status': 'failed', 'message': 'Cart is empty or missing'}, status=400)

        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                total_price += product.price * item['quantity']
            except Product.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

        # Create Stripe checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {'name': f'Order for {email}'},  # Order name as email or user
                        'unit_amount': int(total_price * 100),
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
                    'allowed_countries': ['IN'],  # Replace 'IN' with appropriate country if needed
                },
                success_url=request.build_absolute_uri('/success'),
                cancel_url=request.build_absolute_uri('/cancel'),
            )
        except Exception as e:
            logger.error(f"Stripe checkout session creation failed: {str(e)}")
            return JsonResponse({'status': 'failed', 'message': 'Payment session creation failed'}, status=500)

        return redirect(checkout_session.url, code=303)


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
            logger.error(f"Invalid payload: {str(e)}")
            return JsonResponse({'status': 'failed', 'message': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            return JsonResponse({'status': 'failed', 'message': 'Invalid signature'}, status=400)

        # Log the entire event for debugging
        logger.info(f"Stripe webhook event received: {event}")

        # Handle Stripe event
        event_type = event.get('type')
        event_data = event['data']['object']

        logger.info(f"Processing event type: {event_type}")

        if event_type == 'checkout.session.completed':
            logger.info("Checkout session completed event received")

            # Log the metadata for debugging
            metadata = event_data.get('metadata', {})
            logger.info(f"Metadata: {metadata}")
              
            # Extract user and cart data from metadata
            user_id = metadata.get('user_id')
            shipping_address_id = metadata.get('shipping_address_id')
            cart_data = metadata.get('cart_data')

            if not user_id or not shipping_address_id or not cart_data:
                logger.error("Missing necessary metadata fields (user_id, shipping_address_id, or cart_data)")
                return JsonResponse({'status': 'failed', 'message': 'Missing metadata fields'}, status=400)

            # Retrieve the user and shipping address
            try:
                user = User.objects.get(id=user_id)
                shipping_address = ShippingAddress.objects.get(id=shipping_address_id)
                cart = eval(cart_data)  # Rebuild cart data from string
            except Exception as e:
                logger.error(f"Error retrieving user or shipping address: {str(e)}")
                return JsonResponse({'status': 'failed', 'message': 'Error retrieving user data'}, status=500)

            # Create the order after successful payment
            order = Order.objects.create(
                staff=user,
                date=timezone.now(),
                payment_status='success',
                shipping_address=shipping_address
            )

            total_price = 0
            # Process cart items
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
                    if product.quantity < item['quantity']:
                        return JsonResponse({'status': 'failed', 'message': f'Not enough stock for product {product.name}'}, status=400)
                    product.quantity -= item['quantity']
                    product.save()
                except Product.DoesNotExist:
                    logger.error(f"Product with ID {product_id} does not exist")
                    return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

            # Update order total price
            order.total_price = total_price
            order.save()
            logger.info(f"Order created successfully for Order ID {order.id}")
            
            cart = request.session.get('cart')
            print(f"Cart before clearing: {cart}")    
            if 'cart' in request.session:
                del request.session['cart']
                request.session.save() 
                request.session.modified = True
                print(f"Cart cleared for user: {user.email}")
            else:
                print("No cart is cleared")
            cart_after = request.session.get('cart')
            print(f"Cart before clearing: {cart_after}") 
        elif event_type == 'payment_intent.succeeded':
            logger.info("Payment succeeded for PaymentIntent")
        else:
            logger.info(f"Unhandled event type: {event_type}")

        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

# class ProcessCheckoutView(View):
#     def post(self, request, *args, **kwargs):
#         # Extract data from the request
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         zipcode = request.POST.get('zipcode')
#         phone_no = request.POST.get('phone_no')
#         payment_method_id = request.POST.get('payment_method_id')
#         saved_card_id = request.POST.get('saved_card_id')
#         # print("Request Data:", request.POST)
#         try:
#             # Ensure user exists
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return JsonResponse({'status': 'failed', 'message': 'User not found'}, status=404)
#         user_profile = user.profile

#         if user_profile.stripe_customer_id:
#             stripe_customer_id = user_profile.stripe_customer_id
#         else:
#             # Create a new customer in Stripe if not exists
#             stripe_customer = stripe.Customer.create(email=email)
#             # Save the customer ID in your database (e.g., in the User model)
#             user_profile.stripe_customer_id = stripe_customer.id
#             user_profile.save()
#             stripe_customer_id = stripe_customer.id
#         if not payment_method_id and not saved_card_id:
#             return JsonResponse({'status': 'failed', 'message': 'No payment method or saved card provided'}, status=400)
#         if saved_card_id:
#             pass
#             # If a saved card is selected, use that card ID for the payment
#             payment_method_to_use = saved_card_id
#         elif payment_method_id:
#             # If no saved card is selected, use a new payment method
#             stripe.PaymentMethod.attach(payment_method_id, customer=stripe_customer_id)
#             stripe.Customer.modify(stripe_customer_id, invoice_settings={'default_payment_method': payment_method_id})
#             payment_method_to_use = payment_method_id
#         else:
#             return JsonResponse({'status': 'failed', 'message': 'No payment method provided'}, status=400)

#         # Create shipping address
#         shipping_address = ShippingAddress.objects.create(
#             customer=user,
#             address=address,
#             city=city,
#             state=state,
#             zipcode=zipcode,
#             phone_no=phone_no,
#         )

#         total_price = 0
#         cart = request.session.get('cart', {})
#         if not cart:
#             return JsonResponse({'status': 'failed', 'message': 'Cart is empty or missing'}, status=400)

#         for product_id, item in cart.items():
#             try:
#                 product = Product.objects.get(id=product_id)
#                 total_price += product.price * item['quantity']
#             except Product.DoesNotExist:
#                 return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

#         # Create Stripe checkout session
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                   # Use the selected saved card or new payment method
#                 payment_method_types=['card'],
#                 line_items=[{
#                     'price_data': {
#                         'currency': 'INR',
#                         'product_data': {'name': f'Order for {email}'},  # Order name as email or user
#                         'unit_amount': int(total_price * 100),
#                     },
#                     'quantity': 1,
#                 }],
#                 mode='payment',
#                 metadata={
#                     'user_id': user.id,
#                     'shipping_address_id': shipping_address.id,
#                     'cart_data': str(cart),  # Convert cart data into string for metadata
#                 },
#                 shipping_address_collection={
#                     'allowed_countries': ['IN'],  # Replace 'IN' with appropriate country if needed
#                 },
#                 success_url=request.build_absolute_uri('/success'),
#                 cancel_url=request.build_absolute_uri('/cancel'),
#                 payment_method=payment_method_to_use,
#             )
#         except Exception as e:
#             logger.error(f"Stripe checkout session creation failed: {str(e)}")
#             return JsonResponse({'status': 'failed', 'message': 'Payment session creation failed'}, status=500)

#         return JsonResponse({'status': 'success', 'checkout_url': checkout_session.url})




# @csrf_exempt
# def payment_webhook(request):
#     if request.method == 'POST':
#         payload = request.body
#         endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
#         try:
#             # Verify Stripe signature
#             event = stripe.Webhook.construct_event(
#                 payload, request.headers.get('Stripe-Signature'), endpoint_secret
#             )
#         except ValueError as e:
#             logger.error(f"Invalid payload: {str(e)}")
#             return JsonResponse({'status': 'failed', 'message': 'Invalid payload'}, status=400)
#         except stripe.error.SignatureVerificationError as e:
#             logger.error(f"Invalid signature: {str(e)}")
#             return JsonResponse({'status': 'failed', 'message': 'Invalid signature'}, status=400)

#         # Log the entire event for debugging
#         logger.info(f"Stripe webhook event received: {event}")

#         # Handle Stripe event
#         event_type = event.get('type')
#         event_data = event['data']['object']

#         logger.info(f"Processing event type: {event_type}")

#         if event_type == 'checkout.session.completed':
#             logger.info("Checkout session completed event received")

#             # Log the metadata for debugging
#             metadata = event_data.get('metadata', {})
#             logger.info(f"Metadata: {metadata}")

#             # Extract user and cart data from metadata
#             user_id = metadata.get('user_id')
#             shipping_address_id = metadata.get('shipping_address_id')
#             cart_data = metadata.get('cart_data')

#             if not user_id or not shipping_address_id or not cart_data:
#                 logger.error("Missing necessary metadata fields (user_id, shipping_address_id, or cart_data)")
#                 return JsonResponse({'status': 'failed', 'message': 'Missing metadata fields'}, status=400)

#             # Retrieve the user and shipping address
#             try:
#                 user = User.objects.get(id=user_id)
#                 shipping_address = ShippingAddress.objects.get(id=shipping_address_id)
#                 cart = eval(cart_data)  # Rebuild cart data from string
#             except Exception as e:
#                 logger.error(f"Error retrieving user or shipping address: {str(e)}")
#                 return JsonResponse({'status': 'failed', 'message': 'Error retrieving user data'}, status=500)

#             # Create the order after successful payment
#             order = Order.objects.create(
#                 staff=user,
#                 date=timezone.now(),
#                 payment_status='success',
#                 shipping_address=shipping_address
#             )

#             total_price = 0
#             # Process cart items
#             for product_id, item in cart.items():
#                 try:
#                     product = Product.objects.get(id=product_id)
#                     total_price += product.price * item['quantity']

#                     # Create order item
#                     OrderItem.objects.create(
#                         product=product,
#                         quantity=item['quantity'],
#                         order=order
#                     )
#                     if product.quantity < item['quantity']:
#                         return JsonResponse({'status': 'failed', 'message': f'Not enough stock for product {product.name}'}, status=400)
#                     product.quantity -= item['quantity']
#                     product.save()
#                 except Product.DoesNotExist:
#                     logger.error(f"Product with ID {product_id} does not exist")
#                     return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

#             # Update order total price
#             order.total_price = total_price
#             order.save()
#             logger.info(f"Order created successfully for Order ID {order.id}")

#             # Save the payment method as a "saved card"
#             payment_method_id = event_data.get('payment_method')  # Get the payment method from the event data
#             if payment_method_id:
#                 # Save the card to the user's profile
#                 stripe_payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
#                 user_profile = user.profile
#                 user_profile.stripe_payment_method_id = payment_method_id
#                 print("methodid" ,user_profile.stripe_payment_method_id)
#                 user_profile.save()

#             # Clear cart from the session
#             cart = request.session.get('cart')
#             if 'cart' in request.session:
#                 del request.session['cart']
#                 request.session.save()
#                 request.session.modified = True

#         elif event_type == 'payment_intent.succeeded':
#             logger.info("Payment succeeded for PaymentIntent")
#             payment_method_id = event_data.get('payment_method')  # Get the payment method ID
#             if payment_method_id:
#                 # Save the payment method to the user's profile
#                 stripe_payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
#                 user_profile = user.profile
#                 user_profile.stripe_payment_method_id = payment_method_id
#                 user_profile.save()

#         return JsonResponse({'status': 'success'}, status=200)

#     return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)



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


