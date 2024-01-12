from django.shortcuts import render,redirect,get_object_or_404
from .forms import BrandForm,CategoryForm
from .models import Brand,Category,Product,ProductVariant,Image
from banner.models import Banner
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET





# Create your views here.

#brand list
def admin_brand(request):
    brands = Brand.objects.all()
    return render(request,'c_admin/brand.html',{'brands':brands})


#add brand
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            
    else:
        form = BrandForm()    
    
    return render(request,'c_admin/addbrand.html')


#category list
def admin_category(request):
    categories = Category.objects.all()
    return render(request,'c_admin/category.html',{'categories':categories})
 
 
#add category
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm()       
    return render(request,'c_admin/addcategory.html',{'form':form})


 
# list product
def admin_product_list(request):
    products = Product.objects.all()
    return render(request,'c_admin/productlist.html',{'products':products})


# variant list
def admin_variant_list(request,product_id):
    product = Product.objects.get(id = product_id)
    variants = product.variants.all()
    return render(request,'c_admin/variantlist.html',{'variants':variants,'product':product})  

# add product

def add_product(request):
    
    if request.method == 'POST':
        product_name = request.POST['name']
        brand_id = request.POST['brand']
        category_id = request.POST['category']
        description = request.POST['description']
        specification = request.POST['specification']
        
        brand = Brand.objects.get(id=brand_id)
        category = Category.objects.get(id=category_id)
        
        product = Product.objects.create(
            name=product_name,
            brand=brand,
            category=category,
            description=description,
            specification=specification
        )
        
        variant_materials = request.POST.getlist('variant_material')
        variant_prices = request.POST.getlist('variant_price')
        variant_stocks = request.POST.getlist('variant_stock')
        
        for i in range(len(variant_materials)):
            variant = ProductVariant.objects.create(
                product=product,
                material=variant_materials[i],
                price=variant_prices[i],
                stock_quantity=variant_stocks[i]
            )

            j = 0
            while f'images_{i}_{j}' in request.FILES:
                images = request.FILES.getlist(f'images_{i}_{j}')
                for image in images:
                    Image.objects.create(product_variant=variant, image=image)
                j += 1
        messages.success(request,'added product')
        return redirect('admin_product_list') 
    else:
        # Render the form to add a new product
        brands = Brand.objects.all()
        categories = Category.objects.all()
        return render(request, 'c_admin/addproduct.html', {'brands': brands, 'categories': categories})
    
    
# edit product variant
def edit_product_variant(request,variant_id):
    
    variant = get_object_or_404(ProductVariant,id = variant_id)
    
    if request.method == 'POST':
        material = request.POST['material']
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES.get('image')
        
        variant.material = material
        variant.price = price
        variant.stock_quantity = stock
        variant.save()
        if image is None:
            pass
        else:
            Image.objects.create(product_variant = variant,image = image)
        product_id = variant.product.id
        messages.success(request,'updated')
        return redirect('admin_variant_list',product_id)
        
    
    return render(request,'c_admin/editproduct_variant.html',{'variant':variant})    
        
        
# delete variant image
def delete_variant_image(request,image_id):
    image = get_object_or_404(Image,id = image_id)
    variant_id = image.product_variant.id
    image.delete()
    return redirect('edit_product_variant',variant_id)
      
# soft delete product
def soft_delete_product(request,variant_id):
    variant = get_object_or_404(ProductVariant,id = variant_id)
    if variant.is_available:
        variant.is_available = False
        variant.save()
        product_id = variant.product.id
        return redirect('admin_variant_list',product_id)
    else:
        variant.is_available = True
        variant.save()
        product_id = variant.product.id
        return redirect('admin_variant_list',product_id)
    
# search variant 
def admin_variant_search(request,product_id):
    
    key = request.GET['key']
    variants = ProductVariant.objects.filter(product__id = product_id)
    product = Product.objects.get(id = product_id)
        
    if key is not None:
        variants = variants.filter(material__icontains = key)
            
    context = {
        'variants': variants,
        'key': key,
        'product':product
    }  
    
    return render(request,'c_admin/variantlist.html',context)      
            
    
    
# ====================================================== user ============================================================= !

def user_product_list(request):
    
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    latest_products = Product.objects.all().order_by('created_at')[:3]
    
    
    # get filter parameter from request
    
    category_id = request.GET.get('category_id')
    brand_id = request.GET.get('brand_id')
    
    if category_id:
        category = Category.objects.get(id = category_id)
        products = category.products.all().order_by('-created_at')
        
    if brand_id:
        brand = Brand.objects.get(id = brand_id)
        products = brand.products.all().order_by('-created_at') 
        
        
    # sorting
    
    sorting_criteria = request.GET.get('key')
    
    if sorting_criteria:
        
        if sorting_criteria == 'low_to_high':
            
            # Get all products
            products_all = Product.objects.all()

            # Sort the products based on offer price in ascending order
            products = sorted(products_all, key=lambda x: x.get_product_offer_price())
            
 
        elif sorting_criteria == 'high_to_low':

            # Get all products
            products_all = Product.objects.all()

            # Sort the products based on offer price in ascending order
            products = sorted(products_all, key=lambda x: x.get_product_offer_price(), reverse=True)
            
        elif sorting_criteria == 'latest':
            
            products = Product.objects.all().order_by('-created_at')
            
        else:
            products = Product.objects.all().order_by('-created_at')
            
            
    # Banner
    
    banner_id = request.GET.get('banner_id')
    
    if banner_id:
        
        banner = Banner.objects.get(id = banner_id)
        products = banner.products.all()           
        
    product_count = len(products)       
    
    context = {
        'products':products,
        'categories':categories,
        'brands':brands,
        'latest_products':latest_products,
        'product_count':product_count
    }
 
    return render(request,'user/product/shop.html',context)

# product details
def user_product_details(request,product_id):
    
    product = get_object_or_404(Product,id = product_id)
    
    return render(request,'user/product/productdetails.html',{'product':product})

# user product search
def user_product_search(request):
    key = request.GET['key']
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    latest_products = Product.objects.all().order_by('created_at')[:3]
    
    if key is not None:
        products = Product.objects.filter(name__icontains = key)
        
    product_count = products.count() 
       
    context = {
        'key':key,
        'products':products,
        'categories':categories,
        'brands':brands,
        'latest_products':latest_products,
        'product_count':product_count
    }  
    return render(request,'user/product/shop.html',context)  


@require_GET
def search_suggestions(request):
    query = request.GET.get('query', '')
    suggestions = []
    
    if query:
        products = Product.objects.filter(Q(name__icontains=query))[:10]
        suggestions = [product.name for product in products]

    return JsonResponse({'suggestions': suggestions})



# ============ sorting ============

# sorting by latust
def sorting_by_latust(request):
    
    products = Product.objects.all().order_by('created_at')
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    latest_products = Product.objects.all().order_by('created_at')[:3]
    product_count = products.count()
    
    context = {
        'products':products,
        'categories':categories,
        'brands':brands,
        'latest_products':latest_products,
        'product_count':product_count
    }
 
    return render(request,'user/product/shop.html',context)


# sorting by low to high
def sorting_by_low_to_high(request):
    
    products = Product.objects.all().order_by('created_at')
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    latest_products = Product.objects.all().order_by('created_at')[:3]
    product_count = products.count()
    
    context = {
        'products':products,
        'categories':categories,
        'brands':brands,
        'latest_products':latest_products,
        'product_count':product_count
    }
 
    return render(request,'user/product/shop.html',context)
    

