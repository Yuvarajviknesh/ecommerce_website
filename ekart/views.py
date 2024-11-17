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
from .models import CartItem, Product,Cart,EndUser,Order,OrderItem,Payment
from admin_panel.models import Slide
import re
from django.db.models import Q
from .forms import ForgotPasswordForm, ResetPasswordForm
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
            try:
                user = EndUser.objects.get(email=email)
            except EndUser.DoesNotExist:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
            if check_password(password, user.password):
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
    
    # Search across multiple fields if a query is provided
    if query:
        all_items = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(price__icontains=query)
        )
        if not all_items.exists():  # Check if no results found
            messages.info(request, "Sorry, no products found matching your search.")
            all_items = Product.objects.all()  # Show all products as fallback
    else:
        all_items = Product.objects.all()

    # Retrieve and clean the username from email
    user_email = request.session.get('muser_email', None)
    cleaned_username = None
    if user_email:
        username_part = user_email.split('@')[0]
        cleaned_username = re.sub(r'[^a-zA-Z]', '', username_part)
        request.session['username'] = cleaned_username

        # Save cleaned username to EndUser model if it exists
        try:
            user = EndUser.objects.get(email=user_email)
            user.username = cleaned_username
            user.save()
        except EndUser.DoesNotExist:
            EndUser.objects.create(email=user_email, username=cleaned_username)

    # Pagination
    paginator = Paginator(all_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Retrieve slide images from Slide model
    slides = Slide.objects.all().order_by('order')  # Get slides ordered by the `order` field

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'query': query,
        'cleaned_username': cleaned_username,
        'slides': slides  # Pass slides to the template
    })

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
    user_email = request.session.get('muser_email', None)

    if user_email is None:
        messages.error(request, 'You need to be logged in to add items to the cart.')
        return redirect('login')
    user = get_object_or_404(EndUser, email=user_email)
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1 
    else:
        cart_item.quantity += 1 
    
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

    user = get_object_or_404(EndUser, email=user_email)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = 0
    item_details = []
    
    for item in cart_items:
        price = item.product.offer_price if item.product.offer_price else item.product.price
        item_total = price * item.quantity
        item_details.append({
            'item': item,
            'item_total': item_total
        })
        total_price += item_total

    return render(request, "cart.html", {
        'cart_items': item_details,
        'total_price': total_price,
        'cleaned_username': cleaned_username
    })
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
                reset_token = get_random_string(length=32)
                user.reset_token = reset_token
                user.save()
                reset_link = request.build_absolute_uri(reverse('reset_password', args=[reset_token]))
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    'your-email@example.com',
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
    user = get_object_or_404(EndUser, reset_token=token)
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user.password = make_password(new_password) 
            user.reset_token = None  
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})

def account_details(request):
    user_email = request.session.get('muser_email') 
    if user_email is None:
        messages.error(request, 'You need to be logged in to view account details.')
        return redirect('login') 

    try:
        user = EndUser.objects.get(email=user_email)
        cleaned_username= user.username    
    except EndUser.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('login')  

    return render(request, 'account.html',{'user':user,'cleaned_username':cleaned_username})


from django.utils.crypto import get_random_string

def generate_unique_order_id():
    return get_random_string(length=12).upper()

def checkout(request):
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
    total_price = sum(item.product.offer_price if item.product.offer_price else item.product.price for item in cart_items)

    request.session['total_price_checkout'] = total_price
    cleaned_username = None
    if user_email:
        username_part = user_email.split('@')[0]
        cleaned_username = re.sub(r'[^a-zA-Z]', '', username_part)
    order_id = generate_unique_order_id()

    return render(request, 'checkout.html', {
        'order_id': order_id,
        'total_price': total_price,
        'cart_items': cart_items,
        'cleaned_username': cleaned_username
    })
def create_order(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, "You need to be logged in to place an order.")
        return redirect('login')

    user_email = request.session.get('muser_email')
    if user_email is None:
        messages.error(request, "You need to be logged in to place an order.")
        return redirect('login')

    user = get_object_or_404(EndUser, email=user_email)
    cart = get_object_or_404(Cart, user=user)

    if request.method == 'POST':
        # Extract form data
        contact_number = request.POST.get('contact_number')
        alternate_contact_number = request.POST.get('alternate_contact_number')  # New field
        pincode = request.POST.get('pincode')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')

        # Check for required fields
        if not all([contact_number, street_address, city, state, pincode]):
            messages.error(request, "All required fields must be filled.")
            return redirect('checkout')

        # Validate contact numbers
        if not contact_number.isdigit() or len(contact_number) < 10:
            messages.error(request, "Contact number must be at least 10 digits.")
            return redirect('checkout')

        if alternate_contact_number and (not alternate_contact_number.isdigit() or len(alternate_contact_number) < 10):
            messages.error(request, "Alternate contact number must be at least 10 digits if provided.")
            return redirect('checkout')

        # Create the order
        order = Order.objects.create(
            user=user,
            order_id=generate_unique_order_id(),
            total_price=0,
            status='Pending',
            contact_number=contact_number,
            alternate_contact_number=alternate_contact_number,  # Save the new field
            pincode=pincode,
            street_address=street_address,
            city=city,
            state=state,
        )

        # Calculate total price and create order items
        total_price = 0
        for cart_item in cart.cartitem_set.all():
            item_price = cart_item.product.offer_price if cart_item.product.offer_price else cart_item.product.price
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=item_price,
            )
            total_price += item_price * cart_item.quantity

        order.total_price = total_price
        order.save()

        # Clear the cart
        cart.cartitem_set.all().delete()

        # Store order ID in session and redirect to payment
        request.session['order_id'] = order.order_id
        return redirect('payment_page')

    # Handle invalid request methods
    messages.error(request, "Invalid request method.")
    return redirect('checkout')

from datetime import timedelta
from django.db import transaction

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    user_email = request.session.get("muser_email")

    username_part = user_email.split('@')[0]
    username = re.sub(r'[^a-zA-Z]', '', username_part)
    estimated_delivery_date = order.order_date + timedelta(days=7)

    # Subtract stock for each product in the order
    with transaction.atomic():  # Ensure atomicity to prevent partial updates
        for item in order.items.all():  # Access related OrderItems
            product = item.product
            if product.stock_quantity >= item.quantity:
                product.stock_quantity -= item.quantity
                product.save()
            else:
                # Handle insufficient stock gracefully
                messages.error(request, f"Insufficient stock for {product.title}.")
                return redirect('cart')  # Redirect back to cart or appropriate page

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
        recipient_list=[order.user.email], 
        fail_silently=False,
    )

    return render(request, 'order_confirmation.html', {
        'order_id': order.order_id,
        'total_price': order.total_price,
        'cart_items': order.items.all(),
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
    
    orders = Order.objects.filter(user=user)
    orders_data = []
    for order in orders:
        stages = ["Pending", "Processing", "Shipped", "Delivered"]
        current_stage_index = stages.index(order.status) if order.status in stages else 0
        progress_percentage = (current_stage_index + 1) / len(stages) * 100

        order_items = []
        for item in order.items.all():
            subtotal = item.quantity * item.price
            order_items.append({
                'item': item,
                'subtotal': subtotal,
                'product_image': item.product.image.url if item.product.image else None  # Add product image URL
            })

        orders_data.append({
            'order': order,
            'order_items': order_items,
            'progress_percentage': progress_percentage
        })
        username=request.session.get("username")

    return render(request, 'order_details.html', {
        'orders_data': orders_data,
        'cleaned_username': username,
    })
def payment_page(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "Order not found.")
        return redirect('checkout')

    order = get_object_or_404(Order, order_id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method in ['UPI', 'CARD', 'COD']:
            order.status = 'Paid'
            order.payment_method = payment_method
            order.save()
            payment = Payment.objects.create(
                user=order.user,
                order_id=order.order_id,
                amount=order.total_price,
                payment_method=payment_method,
                status='Completed', 
                transaction_id=f"TXN{order_id}"  
            )

            messages.success(request, f"Payment successful with {payment_method}!")
            return redirect('order_confirmation', order_id=order_id)

        messages.error(request, "Payment failed. Please try again.")
        return redirect('payment_page')

    return render(request, 'payment_page.html', {'order': order})
    