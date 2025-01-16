from djongo import models

# Model for Supplier
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

# Model for Product
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Model for Sale Order
class Saleorder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Cancelled", "Cancelled"), ("Completed", "Completed")])
    sale_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"order {self.id} - {self.product.name}"
    
# Model for Stock Movement
class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ('in', 'Incoming'),
        ('out', 'Outgoing'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update stock levels
        if self.movement_type == 'out' and self.product.stock_quantity < self.quantity:
            raise ValueError("Cannot move stock out: insufficient quantity.")
        if self.movement_type == 'in':
            self.product.stock_quantity += self.quantity
        elif self.movement_type == 'out':
            self.product.stock_quantity -= self.quantity

        self.product.save()
        super().save(*args, **kwargs)
