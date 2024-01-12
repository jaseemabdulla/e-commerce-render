from django.shortcuts import render,redirect,get_object_or_404
from .models import Offer
from django.contrib import messages
from datetime import datetime
from product.models import Category,ProductVariant
from django.core.paginator import Paginator


# Create your views here.


# ======================================================= Admin =====================================================

def offer_list(request):
    offers = Offer.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('-created_at')
    variants = ProductVariant.objects.all().order_by('-created_at')
    paginator = Paginator(variants, per_page=4)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'offers':offers,
        'categories':categories,
        'variants':variants,
        'page_obj':page_obj
    }
    return render(request,'c_admin/offer.html',context)


def add_offer(request):
    if request.method == 'POST':
        offer_title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        discount_percentage = request.POST.get('discount_percentage')
        
        if offer_title.strip() == '':
            messages.error(request,'Fields cannot be blank.')
            return redirect('add_offer')
        
        if start_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date_obj = None
            
        if end_date:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date_obj = None
            
        if Offer.objects.filter(title = offer_title).exists():
            messages.warning(request,'Offer name already exists.')
            return redirect('add_offer')  
        
        if start_date_obj and end_date_obj and start_date_obj > end_date_obj:
            messages.warning(request,'End date must greater than start date.')
            return redirect('add_offer')
        
        offer = Offer.objects.create(
            title=offer_title,
            start_date = start_date_obj,
            end_date = end_date_obj,
            discount_percentage = discount_percentage)  
        messages.success(request,'Offer added succesfully.')
        return redirect('offer_list')
        
    return render(request,'c_admin/add_offer.html')





def apply_offer(request):
    offer_id = request.GET.get('offer_id')
    variant_id = request.GET.get('variant_id')
    category_id = request.GET.get('category_id')
    
    
    offer = Offer.objects.filter(id=offer_id).first()
    product_variant = ProductVariant.objects.filter(id=variant_id).first()
    category = Category.objects.filter(id=category_id).first()
    
    
    if product_variant:
        product_variant.offer = offer
        product_variant.save()
        messages.success(request, 'Offer added successfully to product variant.')
        return redirect('offer_list')
    elif category:
        category.offer = offer
        category.save()
        messages.success(request, 'Offer added successfully to category.')
        return redirect('offer_list')
    else:
        messages.error(request, 'Invalid variant or category ID.')
        return redirect('offer_list')
    

def remove_offer(request,id):
    
    key = request.GET.get('key')
    
    if key == 'variant':
        
        variant = ProductVariant.objects.get(id = id)
        variant.offer = None
        variant.save()
        messages.success(request,'offer removed') 
        
    else:
        
        category = Category.objects.get(id = id)
        category.offer = None
        category.save()
        messages.success(request,'offer removed')
        
    return redirect('offer_list')    
                   