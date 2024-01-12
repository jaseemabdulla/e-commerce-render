from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings




# Create your models here.

# ========== user model =========== !

class UserProfile(AbstractUser):
    
    phone_number = models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return self.username 
    
    def get_whishlist_count(self):
        
        from wishlist.models import Wishlist
        
        whislist = Wishlist.objects.filter(user = self)
        
        return len(whislist)
    
    def get_cartitem_count(self):
        
        from cart.models import Cart,CartItem
        
        cart = Cart.objects.filter(user = self).first()
        cartitems = CartItem.objects.filter(cart = cart)
        
        return len(cartitems)
    
# ========== for otp ============== !

class UserOtp(models.Model):
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 
    time_st = models.DateTimeField(auto_now=True)   
    otp = models.IntegerField()