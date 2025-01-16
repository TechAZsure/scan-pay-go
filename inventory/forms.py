from django import forms
from .models import Product, Supplier, Saleorder

# Form for Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock_quantity', 'description', 'category', 'supplier']

# Form for Supplier
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone_number', 'address']

# Form for Sale Order
class SaleorderForm(forms.ModelForm):
    class Meta:
        model = Saleorder
        fields = ['product', 'quantity']
