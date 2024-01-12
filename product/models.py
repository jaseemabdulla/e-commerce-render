from django.db import models
from django.utils.text import slugify
from offer.models import Offer
from django.utils import timezone
from decimal import Decimal,ROUND_HALF_UP


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=500,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='category/images',blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL,null=True,blank=True)
    
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=500,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='brand/images')
    
    def __str__(self):
        return self.name
        
        
class Product(models.Model):
    name = models.CharField(max_length=50,unique=True)    
    slug = models.SlugField(max_length=50,unique=True,blank=True),
    description = models.TextField(max_length=500,blank=True)
    specification = models.TextField(max_length=500,blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
      
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  
        
    # for geting single product image 
    def get_product_image(self):
        variant = self.variants.filter(is_available = True).first()
        
        if variant:
            product_image = variant.images.first()
            
            if product_image:
                
                return product_image.image.url
            
            else:
                
                return '/static/user/mediass/brand/1.jpg'
            
        else:
             return '/static/user/mediass/brand/1.jpg'   
         
    #for geting all images of product
    
    
    # for geting product variants     
    def get_product_variants(self):
        return self.variants.all()     
    
    
    # for geting product price     
    def get_product_price(self):
        variant = self.variants.filter(is_available = True).first()
        return variant.price  
    
    def get_product_offer_price(self):
        variant = self.variants.filter(is_available = True).first()
        return variant.discounted_price()
    
    
    def has_variants(self):
        return self.variants.exists()
            
            
 
    
class ProductVariant(models.Model):
    material = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=25, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.material
    
    def change_price(self):
        return self.price+150
    
    def get_variant_image(self):
        
        product_image = self.images.first()
        
        if product_image:
                
            return product_image.image.url   
            
        else:
                
            return '/static/user/mediass/brand/1.jpg'  
        
    def discounted_price(self):
        if self.offer:
            disscount_amount = self.price * (Decimal(self.offer.discount_percentage)/100)
            discounted_price = self.price - disscount_amount 
            return discounted_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        elif self.product.category.offer:
            disscount_amount = self.price * (Decimal(self.product.category.offer.discount_percentage)/100)
            discounted_price = self.price - disscount_amount 
            return discounted_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            return self.price
        
    
            

    
class Image(models.Model):
 
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='product/images/')

                       