from django.contrib import admin
from shop.models import Category, Product, Order, OrderItem

admin.site.register([Category, Order, OrderItem])

class ProductAdmin(admin.ModelAdmin):
    model = Product
    exclude = ('discount_price',)
    list_display = ('name', 'category', 'price', 'discount', 'quotity')
    list_filter = ('category',)
    list_display_links = ('name',)
    search_fields = ('name', 'category__name', 'brand')

admin.site.register(Product, ProductAdmin)