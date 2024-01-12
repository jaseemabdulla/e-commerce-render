from django.db import models
from accounts.models import UserProfile
from product.models import Product,ProductVariant
from django.conf import settings

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    is_expired = models.BooleanField(default=False)
    discout_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True, blank=True)
    
    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.cartitems.all())
        return total_price
      
    def get_coupon_discounted_price(self):
        if self.coupon and not self.coupon.is_expired:
            if self.get_total_price() >= self.coupon.minimum_amount:
                return max(self.get_total_price() - self.coupon.discout_price,0)  
        return self.get_total_price()    
     
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='cartitems')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartitems')
    quantity = models.PositiveIntegerField(default=1) 
    
    def get_total_price(self):
        return self.variant.discounted_price() * self.quantity
      
    
    
    
class UserAddress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='addresses')
    address_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    
      
class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),  
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),  
        ('CANCELLED', 'Cancelled'),
    ) 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE,related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='PENDING')
    payment_method = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
       
    def get_orderItem_count(self):
        count = sum(item.quantity for item in self.orderitems.all())
        return count   
      
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderitems')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE,related_name='orderitems')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
        
    
    
    