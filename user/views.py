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
def test(request):
    cart = request.session.get('cart', {})
    print("cart_length", len(cart))
    orders = Order.objects.filter(staff=request.user)
    order_chart = Order.objects.all()
    order_items = OrderItem.objects.select_related('order').all()  # Fetch OrderItem objects
    product = Product.objects.all()
    workers = User.objects.all()
    worker = workers.count()
    order_count = Order.objects.count()
    successful_orders = Order.objects.filter(payment_status='success')
    product_count = Product.objects.count()
    items = Product.objects.filter(quantity__lt=50)
    lowstock_count = items.count()
    order_data = defaultdict(int)

    # Group OrderItems by the date their associated order was created
    for order_item in order_items:
        created_at = order_item.order.created_at  # Use the order's created_at field
        if created_at:
            date_str = created_at.date()  # Use the date part for aggregation
            # print(date_str)
            order_data[date_str] += 1  # Increment count for each OrderItem
    order_dates = sorted(order_data.keys())
    order_quantities = [order_data[date] for date in order_dates]
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
        'order_quantities': order_quantities,  # Pass the order counts to the template
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


def checkout(request):
    cart = request.session.get('cart', {})
    user = request.user
    saved_cards = []  # Fetch saved cards from the user's Stripe profile
    if user.profile.stripe_customer_id:
        saved_cards = stripe.PaymentMethod.list(customer=user.profile.stripe_customer_id, type='card')

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

        try:
            # Ensure user exists
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

        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                total_price += product.price * item['quantity']
                print(f"Product: {product.name}, Quantity: {item['quantity']}, Price: {product.price}")
            except Product.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)

        print(f"Total cart price: {total_price}")
        
        # Handle payment with a saved card
        if selected_card and selected_card != "new":
            print(f"Attempting to create payment intent with card ID: {selected_card}")
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
                    print(f"Order created successfully for Order ID {order.id}")
                    if 'cart' in request.session:
                        del request.session['cart']
                        request.session.modified = True  # Mark the session as modified
                        request.session.save()  # Ensure it gets saved
                        print("Cart cleared in view")
                    return redirect(reverse('success'))
                

                else:
                    print(f"Payment failed with status: {payment_intent.status}")
                    return JsonResponse({'status': 'failed', 'message': 'Payment failed'}, status=400)

            except stripe.error.CardError as e:
                print(f"Stripe CardError: {e.user_message}")
                return JsonResponse({'status': 'failed', 'message': e.user_message}, status=400)
            except stripe.error.StripeError as e:
                print(f"General StripeError: {e.user_message}")
                return JsonResponse({'status': 'failed', 'message': 'An error occurred during payment processing.'}, status=500)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return JsonResponse({'status': 'failed', 'message': 'An unexpected error occurred'}, status=500)

    
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
                success_url=request.build_absolute_uri('/success'),  # Ensure success URL
                cancel_url=request.build_absolute_uri('/cancel'),
                payment_intent_data={
                'setup_future_usage': 'on_session'  # Save the card for future on-session use
                },
                
            )
            
            print(f"Stripe Checkout session created: {checkout_session.id}") 
            if 'cart' in request.session:
                    print(f"Cart before clearing: {request.session['cart']}")
                    del request.session['cart']
                    request.session.save()  # Save the session after clearing the cart
                    request.session.modified = True

            # Redirect to the checkout session URL
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(f"Stripe checkout session creation failed: {str(e)}")
            return JsonResponse({'status': 'failed', 'message': 'Payment session creation failed'}, status=500)


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
            metadata = event_data.get('metadata', {})
            user_id = metadata.get('user_id')
            shipping_address_id = metadata.get('shipping_address_id')
            cart_data = metadata.get('cart_data')

            if not user_id or not shipping_address_id or not cart_data:
                print("Missing necessary metadata fields (user_id, shipping_address_id, or cart_data)")
                return JsonResponse({'status': 'failed', 'message': 'Missing metadata fields'}, status=400)

            # Retrieve the user and shipping address
            try:
                user = User.objects.get(id=user_id)
                shipping_address = ShippingAddress.objects.get(id=shipping_address_id)
                cart = eval(cart_data)  # Rebuild cart data from string
                print(f"Cart data: {cart}")
            except Exception as e:
                print(f"Error retrieving user or shipping address: {str(e)}")
                return JsonResponse({'status': 'failed', 'message': 'Error retrieving user data'}, status=500)

            # Fetch the payment intent from Stripe
            payment_intent_id = event_data.get('payment_intent')
            try:
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            except stripe.error.StripeError as e:
                print(f"Error retrieving payment intent: {str(e)}")
                return JsonResponse({'status': 'failed', 'message': 'Error retrieving payment intent'}, status=500)
            print(f"Cart before clearing: {request.session.get('cart')}")
            if payment_intent.status == 'succeeded':
                print("payment intent succeeded")
                print(f"Cart before clearing in intent: {request.session.get('cart')}")
                # Create the order after successful payment
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
                if 'cart' in request.session:
                    print(f"Cart before clearing: {request.session['cart']}")
                    del request.session['cart']
                    request.session.save()  # Save the session after clearing the cart
                    request.session.modified = True
                    print("Cart cleared in webhook.")
                else:
                    print("No cart to clear in session.")
                
                return JsonResponse({'status': 'success', 'message': 'Order created successfully'}, status=200)
            else:
                print(f"Payment failed with status {payment_intent.status}")
                return JsonResponse({'status': 'failed', 'message': 'Payment failed'}, status=400)

        # Handle other event types if needed
        return JsonResponse({'status': 'success', 'message': 'Event handled successfully'}, status=200)

    # If the request is not a POST request, return a method not allowed response
    return JsonResponse({'status': 'failed', 'message': 'Method not allowed'}, status=405)

# def saved_cards(request):
#     user = request.user
#     stripe_customer_id = user.profile.stripe_customer_id
#     if not stripe_customer_id:
#         return JsonResponse({'status': 'failed', 'message': 'No Stripe customer found'}, status=404)
#     payment_methods = stripe.PaymentMethod.list(
#         customer=stripe_customer_id,
#         type='card'
#     )
#     print('payment_methods' ,payment_methods)
#     return JsonResponse({'status': 'success', 'payment_methods': payment_methods['data']})

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
