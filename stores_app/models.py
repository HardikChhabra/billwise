from django.db import models
from auth_app.models import Store, Customer

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    profit_percent = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    units_sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'name')

    @property
    def selling_price(self):
        return float(self.cost) * (1 + float(self.profit_percent) / 100)

    @property
    def profit_per_unit(self):
        return float(self.selling_price) - float(self.cost)

    @property
    def total_profit(self):
        return self.profit_per_unit * self.units_sold

class BillItem(models.Model):
    bill_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return float(self.price_at_sale) * self.quantity

class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='bills')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(BillItem, related_name='bill')
