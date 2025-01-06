from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product , Order ,Profile
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout ,login as auth_login
from .forms import CreateUserForm , UserUpdateForm , ProfileUpdateForm , ProductForm , OrderForm
from django.contrib.auth.decorators import login_required
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
    order = Order.objects.filter(staff=request.user)
    order_chart = Order.objects.all()
    product = Product.objects.all()
    # if request.method == 'POST':
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         product_name = form.cleaned_data.get('product').name  
    #         messages.success(request, f"'{product_name}' has been added to your order.")
    #         isinstance=form.save(commit=False)
    #         isinstance.staff = request.user
    #         isinstance.save()
    #         return redirect('test')
        
    # else:
    #     form=OrderForm()
    context = {

     'order':order,
    #  'form':form,
     'product':product ,
     'order_chart':order_chart
    }
    return render(request , 'test.html' , context)

@login_required(login_url='login')
def staff(request):
    xyz = Product.objects.all()
    workers = User.objects.all()
    worker = workers.count()
    context = {
        'workers':workers,
        'worker':worker,
        'xyz' : xyz
    }
    return render(request , 'dashboard/staff.html' , context)

@login_required(login_url='login')
def top(request):
    return render(request , 'partials/top.html')

@login_required(login_url='login')
def product(request):
    items = Product.objects.all()
    product_count = Product.objects.count()
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
        'items': items ,
        'form' : form  ,
        'product_count':product_count
    }
    return render(request , 'dashboard/product.html', context)


def order(request):
    order = Order.objects.all()
    order_count = Order.objects.count()
    orders = Order.objects.filter(payment_status='success')
    context = {
        'orders':order,
        'order_count' : order_count,
        'orders': orders
    }
    return render(request , 'dashboard/order.html' , context)


@login_required(login_url='login')
def profile(request):
    return render(request , 'dashboard/profile.html')


@login_required(login_url='login')
def profile_update(request):
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
        'user_form' : user_form,
        'profile_form':profile_form,
        }
    return render(request , 'dashboard/profile_update.html', context)

@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(staff=request.user)
        order, created = Order.objects.get_or_create(staff=request.user)
        items = order.orderitem_set.all()
    else:
        items = []
    context = {
        'items':items
    }

    return render(request , 'dashboard/cart.html' , context)

def delete(request , pk):
    # item = Product.objects.get(id=pk)
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

##############################################################################
# def addto_cart(request, product_id):
#     product = Product.objects.get(id=product_id) 
#     cart = request.session.get('cart', {})

#     if str(product_id) in cart:
#         cart[str(product.id)]['quantity'] += 1
#     else:
#         cart[str(product.id)] = {
#             'name': product.name,
#             'price': str(product.price),
#             'quantity': 1, 
#             'description': product.description,
#             'image': product.image.url 
#         }

#     print("Cart stored in session:", product_id)


#     request.session['cart'] = cart
#     messages.success(request, f'{product.name} has been added to cart')
#     return redirect('test')
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def addto_cart(request, product_id):
    # Fetch the product based on the provided product_id
    product = get_object_or_404(Product, id=product_id)
    
    # Get the current cart from the session
    cart = request.session.get('cart', {})

    # Check the quantity already in the cart for this product
    quantity_in_cart = cart.get(str(product_id), {}).get('quantity', 0)

    # Ensure we don’t add more products than are in stock
    if quantity_in_cart < product.quantity:
        # Product is available, update the cart
        if str(product_id) in cart:
            # Increment the quantity if product already exists in the cart
            cart[str(product_id)]['quantity'] += 1
        else:
            # Add new product to cart
            cart[str(product_id)] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1,
                'description': product.description,
                'image': product.image.url
            }

        # Store the updated cart in the session
        request.session['cart'] = cart
        messages.success(request, f'{product.name} has been added to cart')
    else:
        # Show an error if stock is insufficient
        messages.error(request, f'Not enough stock available for {product.name}')
    
    return redirect('cart')  # Redirect to the cart page after adding to cart

    

def cart(request):
    cart = request.session.get('cart', {})  
    total_price = 0  
    print("Cart items:", cart)
    for item in cart.values():
        item['total_price'] = float(item['price']) * item['quantity']
        total_price += item['total_price']

    context = {'cart_items': cart, 'total_price': total_price}
    return render(request, 'dashboard/cart.html', context)


def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)]['quantity'] += 1
        elif action == 'decrease' and cart[str(product_id)]['quantity'] > 1:
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
    if not cart:
        return redirect('test')
    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
    return render(request, 'dashboard/checkout.html', {
        'cart_items': cart,
        'total_price': total_price
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







#*******************************************


from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.conf import settings
from .models import Order, Product, ShippingAddress, OrderItem
from django.contrib.auth.models import User
stripe.api_key = settings.STRIPE_SECRET_KEY  

class ProcessCheckoutView(View):
    def post(self, request, *args, **kwargs):
        # Get user data from the request
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

        # Create shipping address
        shipping_address = ShippingAddress.objects.create(
            customer=user,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            phone_no=phone_no,
        )
        
        # Create order
        order = Order.objects.create(
            staff=user,
            date=timezone.now(),
            payment_status='failed',
            shipping_address=shipping_address  # Add shipping address here
        )

        total_price = 0
        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({'status': 'failed', 'message': 'Cart is empty or missing'}, status=400)
        # print("cartss", product_id, item)
        for product_id, item in cart.items():
            # print("Processing product:", product_id, "with item:", item)
            try:
                # Ensure the product exists and is correctly retrieved
                product = Product.objects.get(id=product_id)
                total_price += product.price * item['quantity']
                
                # Create order item for each product in the cart
                OrderItem.objects.create(
                    product=product,
                    quantity=item['quantity'],
                    order=order
                )

            except Product.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': f'Product with ID {product_id} does not exist'}, status=404)
            except KeyError:
                return JsonResponse({'status': 'failed', 'message': 'Invalid cart structure or missing quantity for product'}, status=400)

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'INR',
                    'product_data': {
                        'name': f'Order #{order.id}',
                    },
                    'unit_amount': int(total_price * 100),  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=email,  # Send the customer's email to Stripe
            success_url=request.build_absolute_uri('/success'),
            cancel_url=request.build_absolute_uri('/cancel'),
        )

        return redirect(checkout_session.url, code=303)





# Success page
def success(request):
    context = {
        'payment_status': 'success'
    }
    return render(request, 'dashboard/success.html', context)


# Cancel page
def cancel(request):
    context = {
        'payment_status': 'cancel'
    }
    return render(request, 'dashboard/cancel.html', context)


# Webhook to handle payment status from Stripe
@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        payment_status = payload.get('payment_status')
        order_id = payload.get('order_id')

        try:
            # Find the order and update payment status
            order = Order.objects.get(id=order_id)
            if payment_status == 'success':
                order.payment_status = 'success'  # Update to success
            else:
                order.payment_status = 'failed'  # Update to failed
            order.save()

            return JsonResponse({'status': 'success'}, status=200)

        except Order.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Order not found'}, status=404)
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)


