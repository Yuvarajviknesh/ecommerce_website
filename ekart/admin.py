from django.contrib import admin
from .models import Product,Category,EndUser,Cart,CartItem,Order
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','image','description','price','category')
    search_fields=('title','description')
    list_filter=('category','title')

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(EndUser)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)