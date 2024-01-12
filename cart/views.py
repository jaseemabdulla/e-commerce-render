from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import ProductVariant,Product
from cart.models import Cart,CartItem,UserAddress,Order,OrderItem,Coupon
from accounts.models import UserProfile
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.http import HttpResponseRedirect


# Create your views here.

@login_required(login_url='user_login')
def cart_view(request):
    
    user = request.user
    cart, _ = Cart.objects.get_or_create(user = user)
    cart_items = cart.cartitems.all()
    coupons = Coupon.objects.all()
    
    if request.method == 'POST':
        
        code = request.POST.get('coupon')
        coupon = Coupon.objects.filter(code__iexact = code).first()
        
        if not coupon:
            messages.warning(request,'Invalid coupon.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon.is_expired:
            messages.warning(request,'Coupon has been expired..')
            return redirect('cart_view')
          
        if coupon.minimum_amount > cart.get_total_price():
            messages.warning(request,f"Amount should be greater than {coupon.minimum_amount}")
            return redirect('cart_view')
        
        cart.coupon = coupon
        cart.save()
        messages.success(request,'Coupon applied.')
        return redirect('cart_view')
    
    return render(request,'user/cart/cart.html',{'cart_items':cart_items,'cart':cart,'coupons':coupons})   

        
        
# add to cart 
@login_required(login_url='user_login')
def add_to_cart(request,product_id,variant_id = None):
    
    user = request.user
    product = get_object_or_404(Product,pk = product_id)
    cart, _ = Cart.objects.get_or_create(user = user)
    
    variant = None
    if product.has_variants() and variant_id is not None:
        
        variant = get_object_or_404(ProductVariant,pk = variant_id)
        
        if not variant.is_available or variant.stock_quantity <=0:
            messages.warning(request,'out of stock') 
            return redirect('user_product_details',product_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart = cart,product=product,variant=variant)
    
    if not created:
        if cart_item.quantity >= variant.stock_quantity:
            messages.warning(request,'out of stock') 
            return redirect('user_product_details',product_id)
        
        else:
            
            cart_item.quantity += 1
            cart_item.save()
            
    messages.success(request,'added succesfully') 
    return redirect('user_product_details',product_id)   

   


# delete cart item
@login_required(login_url='user_login')
def delete_cart_item(request,cartitem_id):
    cart_item  = CartItem.objects.get(id = cartitem_id)
    cart_item.delete()
    return redirect('cart_view')




# incriment cart item
@login_required(login_url='user_login')
def increment_cart_item(request,cartitem_id):
    cart_item  = CartItem.objects.get(id = cartitem_id)
    if cart_item.quantity < cart_item.variant.stock_quantity:
        cart_item.quantity += 1
        cart_item.save()
        cart_total = cart_item.get_total_price()
        sub_total = cart_item.cart.get_total_price()
        grand_total = cart_item.cart.get_coupon_discounted_price()
        response_date = {
            'quantity': cart_item.quantity,
            'cart_total' : cart_total,
            'sub_total' : sub_total,
            'grand_total' : grand_total
        }
        return JsonResponse(response_date)
    else:
        return JsonResponse({'error': 'out of stock'},status=400)




@login_required(login_url='user_login')
def decrement_cart_item(request,cartitem_id):
    cart_item  = CartItem.objects.get(id = cartitem_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save() 
        cart_total = cart_item.get_total_price()
        sub_total = cart_item.cart.get_total_price()
        grand_total = cart_item.cart.get_coupon_discounted_price()
        response_data = {
            'quantity': cart_item.quantity,
            'cart_total' : cart_total,
            'sub_total' : sub_total,
            'grand_total' : grand_total
        }
        return JsonResponse(response_data)   
    else:
        return JsonResponse({'error':'Quantity must greater than one'}, status=400)

  

#checkout
@login_required(login_url='user_login')
def checkout(request):
    
    user = request.user
    cart,_ = Cart.objects.get_or_create(user = user)
    cart_items = cart.cartitems.all()
    addresses = user.addresses.all()
    
    return render(request,'user/cart/checkout.html',{'cart_items':cart_items,'cart':cart,'addresses':addresses})

    
# add adreess
@login_required(login_url='user_login')
def add_address(request):
    
    if request.method == 'POST':
        
        user = request.user
        
        name = request.POST['name']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        postcode = request.POST['postcode']
        phone = request.POST['phone']
        addressname = request.POST['addressname']
        
        
        choice = [name,street,city,state,postcode,phone,addressname]
        for i in choice:
            if i.strip() == '':
                messages.error(request,'not empty')
                return render(request,'user/cart/add_address.html')
            
             
        UserAddress.objects.create(user = user,address_name = addressname, name = name,street = street,city =city,state = state,postcode = postcode,phone_number =phone)   
        messages.error(request,'not empty')
        return redirect('checkout')
    
    return render(request,'user/cart/add_address.html')


# place order
@login_required(login_url='user_login')
def place_order(request):
    
    user = request.user  
    cart = Cart.objects.get(user = user)
    cart_items = cart.cartitems.all()
    
    
    if request.method =='POST':
        
        address_id = request.POST.get('address')
        
        if address_id is None:
            messages.error(request,'add address')
            return redirect('checkout')
            
        payment_method = request.POST.get('payment_method')
        payment_id = request.POST.get('payment_id')
        address = UserAddress.objects.get(id = address_id)
        total_price = cart.get_coupon_discounted_price()
       
        try:
            with transaction.atomic():  
                
                order = Order.objects.create(user = user,address = address,total_price =total_price,payment_method = payment_method)
                for cart_item in cart_items:
                    product_variant = cart_item.variant
            
                    if cart_item.quantity <= product_variant.stock_quantity:
                
                        order_item = OrderItem.objects.create(order = order,product_variant = product_variant,quantity =cart_item.quantity,total_price = cart_item.get_total_price())
                        product_variant.stock_quantity -= cart_item.quantity
                        product_variant.save()
                
                    else:
                        messages.warning(request,'out of stock')
                        return redirect('cart_view')
                
                order_items = order.orderitems.all()
                cart.delete()
                paymode = request.POST.get('payment_method')
                if paymode == 'Razorpay':
                    
                    return JsonResponse({'status':'order completed',
                                         
                                         'order_id':order.id})
                
                else:
                   
                    messages.success(request,'order completed')
                    return render(request,'user/cart/order_summary.html',{'order':order,'order_items':order_items})
        
        except Exception as e:
            
            messages.error(request, 'An error occurred during order placement. Please try again later.')
            return redirect('cart_view')

def rpay_order_summary(request,order_id):
    order = Order.objects.get(id = order_id)
    order_items = order.orderitems.all()
    return render(request,'user/cart/order_summary.html',{'order':order,'order_items':order_items})   
     
# proceed_to_pay razarpay
@login_required(login_url='user_login')
def proceed_to_pay(request):
    user = request.user
    cart = Cart.objects.get(user = user)
    
    
    total_price = cart.get_coupon_discounted_price()
    
    return JsonResponse({
        
        'total_price':total_price
    })
    
    
# order summary
# @login_required(login_url='user_login')
# def order_summary(request):
#     return render(request,'user/cart/order_summary.html')    

# =================================================== Admin =========================================== !

# order list
def admin_orderlist(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request,'c_admin/orderlist.html',{'orders':orders}) 


# order details
def admin_orderdetails(request,order_id):
    order = Order.objects.get(id = order_id)
    orderitems = order.orderitems.all()
    return render(request,'c_admin/orderdetails.html',{'orderitems':orderitems})

# edit order status
def admin_edit_orderstatus(request,order_id):
    order = Order.objects.get(id = order_id)
    if request.method == 'POST':
        status = request.POST['status']
        order.status = status
        order.save()
        return redirect('admin_orderlist')
            
            
        
    
               