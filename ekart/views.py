from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.hashers import check_password
import logging
from django.utils import timezone
from .models import Product
from django.http import Http404
from django.core.paginator import Paginator
from .models import CartItem, Product,Cart,EndUser,Order,OrderItem
import re
import uuid
from .forms import ForgotPasswordForm, ResetPasswordForm,OrderForm 
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
# items = [
#     {'id': '1', 'image': 'https://m.media-amazon.com/images/I/31uLEZHhMDL.jpg',        'title': 'computer',     'description': 'Lenovo V15 Intel Celeron N4500 15.6" (39.62 cm) FHD (1920x1080) Antiglare 250 Nits Thin and Light Laptop (8GB RAM/256GB SSD/Windows 11 Home/Black/1Y Onsite/1.7 kg), 82QYA00MIN', 'price': 20080},
#     {'id': '2', 'image': 'https://m.media-amazon.com/images/I/71qZERyxy6L._SL1500_.jpg', 'title': 'mobile',     'description': 'Samsung Galaxy S22 5G (Green, 8GB, 128GB Storage) with No Cost EMI/Additional Exchange Offers', 'price': 160000},
#     {'id': '3', 'image': 'https://m.media-amazon.com/images/I/71LRY1j6UHL._SX679_.jpg', 'title': 'Tablet',      'description': 'Xiaomi Pad 6| Qualcomm Snapdragon 870| Powered by HyperOS | 144Hz Refresh Rate| 6GB, 128GB| 2.8K+ Display (11-inch/27.81cm) Tablet| Dolby Vision Atmos| Quad Speakers| Wi-Fi| Gray', 'price': 26999},
#     {'id': '4', 'image': 'https://m.media-amazon.com/images/I/81fxjeu8fdL._SX679_.jpg', 'title': 'iPhone',      'description': 'Apple iPhone 15 Pro Max (256 GB) - Blue Titanium', 'price': 151100},
#     {'id': '5', 'image': 'https://m.media-amazon.com/images/I/81lGxS2ZisL._SX425_.jpg', 'title': 'Alexa',       'description': 'Amazon Echo Dot (5th Gen) | Smart speaker with Bigger sound, Motion Detection, Temperature Sensor, Alexa and Bluetooth| Blue', 'price': 5499},
#     {'id': '6', 'image': 'https://m.media-amazon.com/images/I/71Hd5u7gtuL._SX679_.jpg', 'title': 'Apple Watch', 'description': 'Apple Watch Ultra 2 [GPS + Cellular 49mm] Smartwatch with Rugged Titanium Case & Blue Ocean Band One Size. Fitness Tracker, Precision GPS, Action Button, Extra-Long Battery Life, Bright Retina Display', 'price': 75000},
# ]

def Login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if user exists
            try:
                user = EndUser.objects.get(email=email)
            except EndUser.DoesNotExist:
                messages.error(request, 'Invalid email or password')
                return redirect('login')

            # Authenticate user manually using check_password
            if check_password(password, user.password):
                # Store user email in session and set authenticated flag
                request.session['muser_email'] = user.email
                request.session['is_authenticated'] = True

                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'about.html', {'form': form})

def Sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create and save the user
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  
            user.save()
            messages.success(request, "You have successfully signed up!")
            return redirect('login')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



def index(request):
    query = request.GET.get('search')  
    if query:
        all_items = Product.objects.filter(title__icontains=query)  
    else:
        all_items = Product.objects.all()  
   

    user_email = request.session.get('muser_email', None)
    
    cleaned_username = None
    
    if user_email:
        username_part = user_email.split('@')[0]
        
        cleaned_username = re.sub(r'[^a-zA-Z]', '', username_part)

        request.session['username']= cleaned_username
    
    paginator = Paginator(all_items, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    
    images = [
        {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqNgdTnRQGBHnewy9tTUn1kWxH5Gc4vGxl7g&s", "alt": "Slide 1"},
        {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo_m83owHcDVnalVvx3vif7gtFvCmAQ5sctw&s", "alt": "Slide 2"},
        {"url": "https://www.shutterstock.com/image-vector/special-offer-banner-vector-template-260nw-2474802375.jpg", "alt": "Slide 3"},
        {"url": "https://static.vecteezy.com/system/resources/previews/012/278/243/non_2x/10-10-super-day-sale-banner-design-big-promotion-to-support-the-nine-month-sale-of-products-online-ads-for-the-web-social-media-and-online-shopping-vector.jpg", "alt": "Slide 4"},
        {"url": "https://as2.ftcdn.net/v2/jpg/04/81/13/45/1000_F_481134571_86tGhu4iUxbnpqHrSpgshOnOHqrnw2iA.jpg", "alt": "Slide 5"}
    ]


    
    return render(request, 'home.html', {'page_obj': page_obj, 'query': query, 'cleaned_username': cleaned_username,'images':images})

def detail(request, slug):
    # product = next((item for item in items if item['id'] == str(item_id)), None)
    # logger = logging.getLogger("Testing")
    # logger.debug(f'Item is {product}')
    try:
        item=Product.objects.get(slug_url=slug)
        related_product=Product.objects.filter(category=item.category).exclude(pk=item.id)
    except Product.DoesNotExist:
        raise Http404("Product not found!!!")
    
    user_email = request.session.get('muser_email', None)
    
    cleaned_username = None
    if user_email:
        username_part = user_email.split('@')[0]
        
        cleaned_username = re.sub(r'[^a-zA-Z]', '', username_part)
   
    return render(request, "detail.html", {'item': item,'related_products': related_product,'cleaned_username':cleaned_username})

logger = logging.getLogger(__name__)

def add_to_cart(request, product_id):
    # Ensure the user is authenticated via session
    user_email = request.session.get('muser_email', None)

    if user_email is None:
        messages.error(request, 'You need to be logged in to add items to the cart.')
        return redirect('login')

    # Get the authenticated user object
    user = get_object_or_404(EndUser, email=user_email)

    # Get the product
    product = get_object_or_404(Product, id=product_id)

    # Get or create a cart for the session user (using the `user` field now)
    cart, created = Cart.objects.get_or_create(user=user)

    # Check if the item is already in the cart, if not, create a new one
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if created:
        cart_item.quantity = 1  # Set initial quantity
    else:
        cart_item.quantity += 1  # Increment quantity if already in the cart
    
    cart_item.save()
    
    messages.success(request, f"{product.title} added to your cart!")
    return redirect('cart')

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == "POST":
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f"Quantity for {cart_item.product.title} updated to {quantity}.")
            else:
                messages.error(request, "Quantity must be at least 1.")
        except ValueError:
            messages.error(request, "Invalid quantity value.")
    
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == "POST":
        cart_item.delete()
        messages.success(request, f"{cart_item.product.title} removed from your cart.")
    
    return redirect('cart')

def cart(request):
    user_email = request.session.get('muser_email', None)
    cleaned_username = None
    
    if user_email:
        username_part = user_email.split('@')[0]
        
        cleaned_username = re.sub(r'[^a-zA-Z]', '', username_part)

    if user_email is None:
        messages.error(request, 'You need to be logged in to view the cart.')
        return redirect('login')

    # Get the authenticated user object
    user = get_object_or_404(EndUser, email=user_email)

    # Fetch the cart items for the session user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total price
    total_price = sum(item.total_price() for item in cart_items)
    
    return render(request, "cart.html", {'cart_items': cart_items, 'total_price': total_price,'cleaned_username':cleaned_username})



import random



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    
    return redirect('home') 

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = EndUser.objects.get(email=email)
                
                # Generate a token and save it to the user model
                reset_token = get_random_string(length=32)
                user.reset_token = reset_token
                user.save()
                
                # Build reset link with the reset token
                reset_link = request.build_absolute_uri(reverse('reset_password', args=[reset_token]))

                # Send the email
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    'your-email@example.com',  # Use your actual email here
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "We've sent you an email with instructions to reset your password.")
                return redirect('login')
            except EndUser.DoesNotExist:
                messages.error(request, "Email address not found.")
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request, token):
    # Find the user with the matching reset token
    user = get_object_or_404(EndUser, reset_token=token)
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user.password = make_password(new_password)  # Hash the new password
            user.reset_token = None  # Clear the reset token after use
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})

def account_details(request):
    # Get the user email from the session
    user_email = request.session.get('muser_email')  # Ensure you're using the correct session key

    # Check if the user is logged in
    if user_email is None:
        messages.error(request, 'You need to be logged in to view account details.')
        return redirect('login')  # Redirect to the login page if not logged in

    try:
        # Fetch the user object based on the email
        user = EndUser.objects.get(email=user_email)
        username_part = user_email.split('@')[0]
        cleaned_username = re.sub(r'[^a-zA-Z]', '', username_part)
    except EndUser.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('login')  # Redirect if the user does not exist

    # Render the account details template with the user information
    return render(request, 'account.html',{'user':user})


from django.utils.crypto import get_random_string

def generate_unique_order_id():
    return get_random_string(length=12).upper()

def checkout(request):
    # Check if the user is authenticated
    if not request.session.get('is_authenticated'):
        messages.error(request, "You need to be logged in to checkout.")
        return redirect('login')

    user_email = request.session.get('muser_email')
    user = get_object_or_404(EndUser, email=user_email)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    # Calculate total price
    total_price = sum(item.total_price() for item in cart_items)
    request.session['total_price_checkout'] = total_price

    # Clean username part for display purposes
    cleaned_username = None
    if user_email:
        username_part = user_email.split('@')[0]
        cleaned_username = re.sub(r'[^a-zA-Z]', '', username_part)

    # Generate a unique order ID
    order_id = generate_unique_order_id()

    return render(request, 'checkout.html', {
        'order_id': order_id,
        'total_price': total_price,
        'cart_items': cart_items,
        'cleaned_username': cleaned_username
    })

def create_order(request):
    # Check if the user is authenticated
    if not request.session.get('is_authenticated'):
        messages.error(request, "You need to be logged in to place an order.")
        return redirect('login')

    # Retrieve the user and cart
    user_email = request.session.get('muser_email', None)
    if user_email is None:
        messages.error(request, 'You need to be logged in to place an order.')
        return redirect('login')

    user = get_object_or_404(EndUser, email=user_email)
    cart = get_object_or_404(Cart, user=user)

    if request.method == 'POST':
        # Get order details from form
        contact_number = request.POST.get('contact_number')
        pincode = request.POST.get('pincode')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')

        if not all([contact_number, street_address, city, state, pincode]):
            messages.error(request, "All fields are required.")
            return redirect('checkout')

        # Create Order
        order = Order.objects.create(
            user=user,
            order_id=generate_unique_order_id(),
            total_price=0,
            status='Pending',
            contact_number=contact_number,
            pincode=pincode,
            street_address=street_address,
            city=city,
            state=state,
        )

        # Add cart items to the order
        total_price = 0
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
            total_price += cart_item.total_price()

        # Update order total price
        order.total_price = total_price
        order.save()

        # Clear the cart
        cart.cartitem_set.all().delete()
        request.session ['order_id']= order.order_id

        messages.success(request, f"Order {order.order_id} created successfully!")
        return redirect('order_confirmation', order_id=order.order_id)

    messages.error(request, "Invalid request method.")
    return redirect('checkout')
from datetime import timedelta


def order_confirmation(request, order_id):
    # Fetch the order object
    order = get_object_or_404(Order, order_id=order_id)
    user_email = request.session.get("muser_email")

    username_part = user_email.split('@')[0]
    username = re.sub(r'[^a-zA-Z]', '', username_part)


    # Calculate estimated delivery date (7 days from order date)
    estimated_delivery_date = order.order_date + timedelta(days=7)

    # Send confirmation email
    send_mail(
        subject="Order Confirmation",
        message=(
            f"Hello {username},\n\n"
            f"Thank you for your order! Your order ID is {order.order_id}.\n"
            f"The total price is ₹{order.total_price}.\n"
            f"Your order is expected to be delivered by {estimated_delivery_date.strftime('%Y-%m-%d')}.\n\n"
            "Thank you for shopping with us!"
        ),
        from_email="your_email@gmail.com",
        recipient_list=[order.user.email],  # Assuming the order has a related user with an email
        fail_silently=False,
    )

    # Render the order confirmation page
    return render(request, 'order_confirmation.html', {
        'order_id': order.order_id,
        'total_price': order.total_price,
        'cart_items': order.items.all(),  # Use 'items' related name
        'cleaned_username': username,
        'estimated_delivery_date': estimated_delivery_date,
    })


def order_details(request):
    user_email = request.session.get("muser_email")

    if not user_email:
        messages.error(request, "You need to be logged in to view your order details.")
        return redirect('login')
    
    try:
        user = EndUser.objects.get(email=user_email)
    except EndUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')
    
    # Fetch all orders for the user
    orders = Order.objects.filter(user=user)

    # Process each order to calculate progress and subtotals for order items
    orders_data = []
    for order in orders:
        stages = ["Pending", "Processing", "Shipped", "Delivered"]
        current_stage_index = stages.index(order.status) if order.status in stages else 0
        progress_percentage = (current_stage_index + 1) / len(stages) * 100

        # Calculate the subtotal for each order item
        order_items = []
        for item in order.items.all():
            subtotal = item.quantity * item.price
            order_items.append({
                'item': item,
                'subtotal': subtotal
            })

        orders_data.append({
            'order': order,
            'order_items': order_items,
            'progress_percentage': progress_percentage
        })
        username=request.session.get("username")

    return render(request, 'order_details.html', {
        'orders_data': orders_data,
        'cleaned_username':username,
    })
