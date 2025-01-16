from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db import DatabaseError
from .forms import ProductForm, SupplierForm, SaleorderForm
from .models import Product, Supplier, Saleorder, StockMovement
from decimal import Decimal

# View to render the home page
def home(request):
    return render(request, 'base.html')

# View to add a new product
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity')
        supplier_name = request.POST.get('supplier')

        # Fetch or create the supplier
        supplier, created = Supplier.objects.get_or_create(name=supplier_name)

        # Create the product
        Product.objects.create(
            name=name,
            price=price,
            description=description,
            category=category,
            stock_quantity=stock_quantity,
            supplier=supplier
        )
        return redirect('list_products')  # Replace with your product listing view name
    
    return render(request, 'add_product.html')

# View to list all products
def list_products(request):
    products = Product.objects.all()  # Get all products from the database
    return render(request, 'list_product.html', {'products': products})

# View to add a new supplier
def add_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        # Check for duplicates first
        if Supplier.objects.filter(name=name).exists():
            messages.error(request, 'A supplier with this name already exists.')
        elif Supplier.objects.filter(email=email).exists():
            messages.error(request, 'A supplier with this email already exists.')
        elif Supplier.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'A supplier with this phone number already exists.')
        else:
            try:
                # Save the new supplier
                Supplier.objects.create(name=name, email=email, phone_number=phone_number, address=address)
                messages.success(request, 'Supplier added successfully.')
                return redirect('list_suppliers')  # Redirect to the supplier list page after successful add
            except DatabaseError as e:
                # This will capture any database-specific error (such as unique constraint violation)
                messages.error(request, f"Database error: {str(e)}")
            except Exception as e:
                # General exception handling for unexpected errors
                messages.error(request, f"Unexpected error: {str(e)}")

    return render(request, 'add_supplier.html')

# View to list all suppliers
def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'list_suppliers.html', {'suppliers': suppliers})

# View to create a new sale order
def create_sale_order(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity"))
        product = Product.objects.get(id=product_id)

        if product.stock_quantity >= quantity:
            total_price = product.price * quantity
            Saleorder.objects.create(
                product_id=product_id,
                quantity=quantity,
                total_price=total_price,
                status="Pending"
            )
            product.stock_quantity -= quantity
            product.save()
            messages.success(request, "Sale order created successfully.")
            return redirect("list_sale_orders")
        else:
            messages.error(request, "Insufficient stock for this product.")
    
    products = Product.objects.all()
    return render(request, "create_sale_order.html", {"products": products})

# View to list all sale orders
def list_sale_orders(request):
    sale_orders = Saleorder.objects.all()
    return render(request, 'list_sale_orders.html', {'sale_orders': sale_orders})

def add_stock_movement(request):
    products = Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product')
        movement_type = request.POST.get('movement_type')
        quantity_str = request.POST.get('quantity', '').replace('“', '').replace('”', '')  # Remove fancy quotes
        quantity = Decimal(quantity_str)

        product = get_object_or_404(Product, id=product_id)

        try:
            stock_movement = StockMovement(
                product=product,
                movement_type=movement_type,
                quantity=quantity
            )
            messages.success(request, "Stock movement recorded successfully.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('add_stock_movement')

    return render(request, 'add_stock_movement.html', {'products': products})

def cancel_sale_order(request, order_id):
    sale_order = Saleorder.objects.get(id=order_id)
    sale_order.status = "Cancelled"
    sale_order.product.stock_quantity += sale_order.quantity
    sale_order.product.save()
    sale_order.save()
    messages.success(request, "Sale order cancelled successfully.")
    return redirect("list_sale_orders")

def complete_sale_order(request, order_id):
    sale_order = Saleorder.objects.get(id=order_id)
    if sale_order.status == "Pending":
        sale_order.status = "Completed"
        sale_order.save()
        messages.success(request, "Sale order marked as completed.")
    else:
        messages.error(request, "Only pending orders can be completed.")
    return redirect("list_sale_orders")

def stock_level_check(request):
    products = Product.objects.all()
    return render(request, "stock_level_check.html", {"products": products})
