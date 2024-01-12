from django.shortcuts import render
from banner.models import Banner
from product.models import Category,Brand,Product

# Create your views here.

def user_home(request):
    
    actived_banners = Banner.objects.filter(is_active = True)
    categories = Category.objects.all()[:4]
    brands = Brand.objects.all()[:4]
    products = Product.objects.all()
    
    context = {
        'actived_banners':actived_banners,
        'categories':categories,
        'brands':brands,
        'products':products
    }
    
    
    return render(request,'user/home.html',context)