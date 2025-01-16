from django.contrib import admin
from .models import Supplier, Product, Saleorder, StockMovement

# Registering the models to the Django Admin
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'supplier', 'category')
    search_fields = ('name', 'category')
    list_filter = ('supplier', 'category')

class SaleorderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price', 'sale_date')
    list_filter = ('sale_date',)
    search_fields = ('product__name',)

class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'movement_type', 'date')
    list_filter = ('movement_type', 'date')
    search_fields = ('product__name',)

# Register models with custom Admin

