from django.db import models
from accounts.models import UserProfile
from product.models import ProductVariant

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlists')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)