from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone

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
    date_time = models.DateTimeField(auto_now_add=True)
    slug_url = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    stock_quantity=models.IntegerField(default=0)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    material = models.CharField(max_length=100)
    warranty = models.IntegerField()  

    def save(self, *args, **kwargs):
        self.slug_url = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EndUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    reset_token = models.CharField(max_length=32, blank=True, null=True)  
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
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    street_address = models.CharField(max_length=255, blank=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')  
    contact_number = models.CharField(max_length=15, blank=True)  
    pincode = models.CharField(max_length=10, blank=True) 
    street_address = models.CharField(max_length=255, blank=True)  
    city = models.CharField(max_length=100, blank=True)  
    state = models.CharField(max_length=100, blank=True)  
    order_id = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return f"Order #{self.id} by {self.user.email} on {self.order_date.strftime('%Y-%m-%d')} (Total: {self.total_price})"

    class Meta:
        ordering = ['-order_date']  

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ], default='Pending')

    def __str__(self):
        return f"Payment for {self.order.order_id} - {self.status}"