from django.db import models
from product.models import Product

# Create your models here.

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    title = models.CharField(max_length=100)
    description1 = models.TextField()
    description2 = models.TextField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='banners')
