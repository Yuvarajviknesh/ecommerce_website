from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ekart.models import Product,EndUser,Order,OrderItem
from .forms import ProductForm
from xhtml2pdf import pisa
from django.template.loader import get_template
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

@login_required
def admin_products(request):
    products = Product.objects.all()
    if request.method == 'POST' and 'add_product' in request.POST:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm()

    return render(request, 'admin_products.html', {
        'products': products,
        'form': form,
    })

# View to handle editing a product
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

# View to handle deleting a product
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('admin_products')
    return render(request, 'delete_confirmation.html', {'product': product})
@login_required
def sales(request):
    # Fetch all orders with related items (products)
    orders = Order.objects.all().prefetch_related('items')

    sales_data = []
    for order in orders:
        for item in order.items.all():
            sales_data.append({
                'order': order,
                'product': item.product,
                'quantity': item.quantity,
                'total_price': item.quantity * item.price,
            })

    context = {
        'sales': sales_data,
    }

    return render(request, 'admin_sales.html', context)

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            order.status = status
            order.save()
    
    return redirect('sales')  # Redirect to the sales view

@login_required
def update_delivery_date(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        estimated_delivery_date = request.POST.get('estimated_delivery_date')
        if estimated_delivery_date:
            order.estimated_delivery_date = estimated_delivery_date
            order.save()
    
    return redirect('sales') # View to generate a print receipt
@login_required
def print_receipt(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    # Generate a printable HTML response for the receipt
    context = {
        'order': order,
    }
    return render(request, 'print_receipt.html', context)

# Admin Customers View (Example of how to fetch and display customer data)
@login_required
def admin_customers(request):
    customers = EndUser.objects.all()  # Retrieve all users (or your custom customer model)
    return render(request, 'admin_customers.html', {'customers': customers})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('adminpanel')  

def download_receipt_pdf(request, order_id):
    """
    Download the order receipt as a PDF file.
    """
    order = get_object_or_404(Order, order_id=order_id)
    
    # Load the HTML template and render it with order data
    template = get_template("print_receipt.html")
    html = template.render({"order": order})
    
    # Create an HttpResponse object with PDF headers
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="Order_{order_id}_Receipt.pdf"'
    
    # Generate PDF and handle errors
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        # Render the error on the same page if PDF generation fails
        return render(request, "print_receipt.html", {"order": order, "error_message": "There was an error generating the PDF."})
    
    return response
