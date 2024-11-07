from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ekart.models import Product,Cart,CartItem,EndUser,Order

def admin_panel(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Check if user is an admin (staff member)
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'adminpanel.html')

@login_required
def admin_dashboard(request):
    # Example data for the dashboard statistics
    total_sales = 12500
    products_in_stock = Product.objects.count()
    new_orders = Order.objects.count()

    context = {
        'total_sales': total_sales,
        'products_in_stock': products_in_stock,
        'new_orders': new_orders
    }

    return render(request, 'admin_dashboard.html', context)


# Admin Products View
@login_required
def admin_products(request):
    # Fetch all products
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'admin_products.html', context)


# Admin Sales View
@login_required
def admin_sales(request):
    # Fetch all cart items (representing sales in this example)
    sales = CartItem.objects.all()

    context = {
        'sales': sales
    }

    return render(request, 'admin_sales.html', context)


# Admin Customers View (Example of how to fetch and display customer data)
@login_required
def admin_customers(request):
    customers = EndUser.objects.all()  # Retrieve all users (or your custom customer model)
    return render(request, 'admin_customers.html', {'customers': customers})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('adminpanel')  