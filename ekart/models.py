from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create Category model
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# Create Product model
class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Product/')
    description = models.TextField()
    price = models.IntegerField()
    offer_price = models.IntegerField(null=True, blank=True)  # Add offer_price
    date_time = models.DateTimeField(auto_now_add=True)
    slug_url = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    stock_quantity = models.IntegerField(default=0)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    warranty = models.CharField(max_length=50)  

    def save(self, *args, **kwargs):
        self.slug_url = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class EndUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    reset_token = models.CharField(max_length=32, blank=True, null=True)  
    username = models.CharField(max_length=150, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Cart(models.Model):
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('EndUser', on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    contact_number = models.CharField(max_length=15, blank=True)
    alternate_contact_number = models.CharField(max_length=15, blank=True)  # Added field
    pincode = models.CharField(max_length=10, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    order_id = models.CharField(max_length=100, unique=True, editable=False)
    estimated_delivery_date = models.DateField(null=True)

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.email} on {self.order_date.strftime('%Y-%m-%d')} (Total: {self.total_price})"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = str(uuid.uuid4().hex[:10])  # Generate a unique order_id if not provided
        super(Order, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['order_id']),
            models.Index(fields=['status']),
            models.Index(fields=['order_date']),
        ]

    def items(self):
        return self.orderitem_set.all()  # Access related items using the 'items' related name
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # Use related_name 'items'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} at {self.price} each"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI (Google Pay)'),
        ('CARD', 'Card'),
        ('COD', 'Cash on Delivery'),
    ]
    
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True) 
    status = models.CharField(max_length=20, default='Pending')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_method} - {self.status}"