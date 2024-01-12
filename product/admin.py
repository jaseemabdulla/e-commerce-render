from django.contrib import admin
from .models import Product,ProductVariant,Category,Brand,Image
# Register your models here.


admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Image)
