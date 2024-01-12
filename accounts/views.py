from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import UserProfile,UserOtp
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash,get_user_model
from django.contrib import messages
from cart.models import Order,OrderItem,UserAddress
from wallet.models import Wallet
from django.contrib.auth.decorators import login_required
from product.models import Product,ProductVariant
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncMonth


# ==== for validation and verification ===== !
import random
from django.core.mail import send_mail
from django.conf import settings
import re
from django.core.exceptions import ValidationError
from random import randint
from .utils import send_otp_via_sms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import base64


# ========= for class

from django.template.loader import render_to_string
from xhtml2pdf import pisa


# for invoice

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Create your views here.

def user_signin(request):
    
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        
        if get_otp:
            
            get_email = request.POST.get('email')
            usr = UserProfile.objects.get(email = get_email)
            
            if int(get_otp) == UserOtp.objects.get(user = usr).otp:
                usr.is_active = True
                usr.save()
                login(request,usr)
                UserOtp.objects.filter(user = usr).delete()
                return redirect('user_home')
            else:
                messages.error(request,'wrong otp')
                return render(request,'user/account/register.html')
            
        else:
        
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            phone = request.POST['phone']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            
            # null value check
            
            check = [firstname,lastname,email,phone,username,password1,password2]
            
            for values in check:
                
                if values == '':
                    context = {
                        'pre_firstname':firstname,
                        'pre_lastname' :lastname,
                        'pre_email': email,
                        'pre_phone': phone,
                        'pre_username':username,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'user/account/register.html',context)
                else:
                    pass
            
            # username check    
                
            result = validate_username(username)
            
            if result is not False:
                context = {
                        'pre_firstname':firstname,
                        'pre_lastname' :lastname,
                        'pre_email': email,
                        'pre_phone': phone,
                        'pre_username':username,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                messages.info(request,result)
                return render(request,'user/account/register.html',context)
            else:
                pass
            
            #email check
            
            resemail = email_validations(email)
            
            if resemail is False:
                context = {
                        'pre_firstname':firstname,
                        'pre_lastname' :lastname,
                        'pre_email': email,
                        'pre_phone': phone,
                        'pre_username':username,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                
                messages.info(request,'enter valied email')
                return render(request,'user/account/register.html',context)
            else:
                pass
            
            # phone number check
            
            resphone = phone_number_validation(phone)
            
            if resphone is False:
                context = {
                        'pre_firstname':firstname,
                        'pre_lastname' :lastname,
                        'pre_email': email,
                        'pre_phone': phone,
                        'pre_username':username,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                
                messages.info(request,'enter valied phone number')
                return render(request,'user/account/register.html',context)
            else:
                pass
            
            # password check
            
            respassword = pass_validation(password1)
            
            if respassword is False:
                context = {
                        'pre_firstname':firstname,
                        'pre_lastname' :lastname,
                        'pre_email': email,
                        'pre_phone': phone,
                        'pre_username':username,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                
                messages.info(request,'enter a strong password')
                return render(request,'user/account/register.html',context)
            else:
                pass
            
            if password1 == password2:
                
                try:
                    UserProfile.objects.get(email = email)
                except:
                    usr = UserProfile(first_name = firstname,last_name = lastname,email = email,phone_number = phone,username = username)    
                    usr.set_password(password1)
                    usr.is_active = False
                    usr.save()
                    
                    user_otp = random.randint(100000,999999)
                    UserOtp.objects.create(user = usr,otp = user_otp)
                    mess=f'Hello \t{usr.username},\nYour OTP to verify your account for LojLove furnitures is {user_otp}\n Thanks You!'
                    
                    send_mail(
                        
                        "Welcome to LojLove furnitures , verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        
                        fail_silently=False
                      )
                    return render(request,'user/account/register.html',{'otp':True,'usr':usr})
                else:
                    
                    context = {
                        'pre_firstname':firstname,
                        'pre_lastname' :lastname,
                        'pre_email': email,
                        'pre_phone': phone,
                        'pre_username':username,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                
                messages.info(request,'email already exists')
                return render(request,'user/account/register.html',context)
            
            else:
                context = {
                        'pre_firstname':firstname,
                        'pre_lastname' :lastname,
                        'pre_email': email,
                        'pre_phone': phone,
                        'pre_username':username,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                
                messages.info(request,'password not match')
                return render(request,'user/account/register.html',context)
            
    else:
        return render(request,'user/account/register.html')
    


# ===== username validation ======= !

def validate_username(username):
    if not re.match(r'^[a-zA-Z\s]*$',username):
        return 'username should only content alphabets'
    elif UserProfile.objects.filter(username = username).exists():
        return 'username already exist'
    else:
        return False
        
# ===== email validation ========= !

def email_validations(email):

    from django.core.validators import validate_email

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# ====== password validation ====== !

def pass_validation(password):
    
    from django.contrib.auth.password_validation import validate_password
    
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False   

# phone number validation
    
def phone_number_validation(phone):
    if len(phone) == 10 and phone.isdigit():
        return True
    else:
        return False           
    

def user_login(request):
    if request.method == 'POST':
        
        
        
        usname = request.POST.get('username')
        paword = request.POST.get('password')
        
        
        u = get_object_or_404(UserProfile,username = usname)
        if not u.is_active:
            messages.error(request,'you are blocked')
            return render(request,'user/account/login.html')
        
        # validation  
        
        
        if usname.strip() == '' or paword.strip() == '':
            messages.error(request,'not empty')
            return render(request,'user/account/login.html')
        
        user = authenticate(username = usname,password = paword)
            
        if user is not None:
            login(request,user)
            return redirect('user_home')
        else:
            messages.error(request,'invalid input')
            return render(request,'user/account/login.html')
            
                
    else:
        return render(request,'user/account/login.html')
    
    
def user_logout(request):
    logout(request)
    return redirect('user_home')  


# user profile
@login_required(login_url='user_login')
def user_profile(request):
    
    return render(request,'user/account/profile/account_home.html')  


# user orders
@login_required(login_url='user_login')
def user_orders(request):
    user = request.user
    orders = Order.objects.filter(user = user).order_by('-created_at')
    return render(request,'user/account/profile/orders.html',{'orders':orders}) 


# cancel order
@login_required(login_url='user_login')
def user_cancel_order(request,order_id):
    user = request.user
    order = Order.objects.get(id =order_id)
    order.status = 'CANCELLED'
    order.save()
    wallet_amount = order.total_price
    wallet, created = Wallet.objects.get_or_create(user=user, defaults={'amount': wallet_amount})
    if created: 
        pass
    else:
        wallet.amount += wallet_amount
        wallet.save()
        
    messages.success(request,'order canceled succesfully') 
    return redirect('user_orders')    




# order details
@login_required(login_url='user_login')
def user_orderdetails(request,order_id):
    order = Order.objects.get(id = order_id)
    order_items = OrderItem.objects.filter(order = order)
    return render(request,'user/account/profile/orderdetails.html',{'order_items':order_items,'order_id':order_id})


# user address
@login_required(login_url='user_login')
def user_address(request):
    user = request.user
    addresses = UserAddress.objects.filter(user = user)
    return render(request,'user/account/profile/address.html',{'addresses':addresses})


# user details
@login_required(login_url='user_login')
def user_details(request):
    user = request.user
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        passward = request.POST.get('password')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        
        if not user.check_password(passward):
            messages.error(request,'wrong password')
            return redirect('user_details')
        
        if first_name:
            user.first_name = first_name
            
        if last_name:
            user.last_name = last_name
          
        if username:
            result = validate_username(username)
            if user.username == username:
                pass
            elif result is not False:
                messages.error(request,result) 
                return redirect('user_details')
            else:
                user.username = username
               
        if new_password1 and new_password2:
            
            if new_password1 == new_password2:
                user.set_password(new_password1) 
                update_session_auth_hash(request,user)
                
            else:
                messages.error(request,'new password not match')
                return redirect('user_details')
                       
        user.save()
        messages.success(request,'User details successfully updated.')
        return redirect('user_details')
        
    return render(request,'user/account/profile/details.html',{'user':user}) 


# login with otp
def login_with_otp(request):
    
    
    if request.method == 'POST':
        
        get_otp = request.POST.get('otp')      
        if get_otp:
            
            phone_number = request.POST['phone']
            user = UserProfile.objects.get(phone_number = phone_number)
            
            if int(get_otp) == UserOtp.objects.get(user = user).otp:
                login(request,user)
                UserOtp.objects.filter(user = user).delete()
                return redirect('user_home')
            else:
                messages.error(request,'wrong otp')
                return redirect('login_with_otp')
            
        else:
            
            phone_number = request.POST['phone']
            
            try:
                user = UserProfile.objects.get(phone_number = phone_number) 
                
            except UserProfile.DoesNotExist:
                
                messages.error(request,'invalid cresential')
                return redirect('login_with_otp')
            
            otp = str(randint(100000,999999))
            user_otp = UserOtp.objects.create(user = user,otp = otp)
            phone = '+91'+phone_number
            send_otp_via_sms(phone,otp)
            return render(request,'user/account/loginotp.html',{'otpp':True,'user':user})
     
    else:
        return render(request,'user/account/loginotp.html')                   
        
# ========================================== Class based view ===============================

# UserModel = get_user_model()

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'user/account/forgot-password/forgot-password.html'
#     success_url = reverse_lazy('password_reset')
    
#     def form_valid(self,form):
        
#         self.request.session['reset_email'] = form.cleaned_data['email']
#         return super().form_valid(form)
          
    
# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'user/account/forgot-password/reset_done.html' 
#     success_url = reverse_lazy('user_login')
#     form_class = SetPasswordForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.get_user(uidb64=self.kwargs['uidb64'])
#         if user is not None and self.request.session.get('reset_email') == user.email:
#             context['form'] = self.form_class(user=user)  # Pass the user argument
            
#         return context

#     def get_user(self, uidb64):
#         try:
#             return UserModel._default_manager.get(pk=uidb64)
#         except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#             return None

#     def post(self, *args, **kwargs):
#         user = self.get_user(uidb64=self.kwargs['uidb64'])
#         if user is not None and self.request.session.get('reset_email') == user.email:
#             return super().post(*args, **kwargs)
#         return redirect('user_login')


  

# forgot password

UserModel = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = UserModel.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            user_pk_bytes = user.pk.to_bytes((user.pk.bit_length() + 7) // 8, byteorder='big')
            uidb64 = base64.urlsafe_b64encode(user_pk_bytes).decode('utf-8')
            domain = get_current_site(request).domain
            reset_url = reverse('reset_password', kwargs={'uidb64': uidb64, 'token': token})
            reset_link = f"http://{domain}{reset_url}"
            send_mail(
                subject="Password Reset",
                message=f"Click the following link to reset your password: {reset_link}",
                from_email="noreply@example.com",
                recipient_list=[user.email],
            )
            return redirect('password_reset_done')
    return render(request, 'user/account/forgot-password/forgot-password.html')


def reset_password(request, uidb64, token):
    try:
        uid_bytes = base64.urlsafe_b64decode(uidb64.encode('utf-8'))
        uid = int.from_bytes(uid_bytes, byteorder='big')
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            return redirect('password_reset_complete')
        return render(request, 'user/account/forgot-password/reset_password.html')
    else:
        return redirect('password_reset_invalid')



def password_reset_done(request):
    return render(request, 'user/account/forgot-password/password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'user/account/forgot-password/password_reset_complete.html')

def password_reset_invalid(request):
    return render(request, 'user/account/forgot-password/password_reset_invalid.html')


# invoice download

def generate_invoice_pdf(request, order_id):
    order = Order.objects.get(id = order_id)
    template = 'user/account/profile/invoice_template.html'
    context = {
        'order': order,
        'year': timezone.now().year
        }
    html_content = render_to_string(template, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    pdf_status = pisa.CreatePDF(html_content, dest=response)
    if pdf_status.err:
        return HttpResponse("Error generating PDF", status=500)
    return response

# =================================================== Admin ===================================== !

def admin_login(request):
    if not request.user.is_superuser:
        return redirect('user_home')
    orders = Order.objects.filter(status = 'DELIVERED').order_by('-updated_at')
    revenue = sum(item.total_price for item in orders)
    count = orders.count()
    products_count = Product.objects.all().count()
    variant_count = ProductVariant.objects.all().count()
    
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year
    current_week = current_date.isocalendar()[1]
    current_day = timezone.now().date()
    
    revenue_mounth = Order.objects.filter(
        created_at__year = current_year,
        created_at__month = current_month,
        status = 'DELIVERED'
    ).aggregate(total_price_sum = Sum('total_price'))['total_price_sum']
    
    revenue_week = Order.objects.filter(
        created_at__year = current_year,
        created_at__month = current_month,
        created_at__week = current_week,
        status = 'DELIVERED'
    ).aggregate(total_price_sum = Sum('total_price'))['total_price_sum']
    
    revenue_day = Order.objects.filter(
        created_at__date = current_day,
        status = 'DELIVERED'
    ).aggregate(total_price_sum = Sum('total_price'))['total_price_sum']
    
    # for chart 
    # Create a list to hold total prices for each month
    monthly_total_prices = []

    # Iterate through each month (from January to December)
    for month_number in range(1, 13):
        total_price = Order.objects.filter(
            created_at__month=month_number,
            status='DELIVERED',
            created_at__year=current_year
        ).aggregate(total_price_sum=Sum('total_price'))['total_price_sum'] or 0
    
        total_price_float = float(total_price)
        monthly_total_prices.append(total_price_float)
        
        
    # for pie chart 
    cod_count = len([item for item in orders if item.payment_method == 'COD']) 
    razorpay_count = len([item for item in orders if item.payment_method == 'Razorpay'])
    
    context = {
        'revenue':revenue,
        'count':count,
        'products_count':products_count,
        'variant_count':variant_count,
        'revenue_mounth':revenue_mounth,
        'revenue_week' :revenue_week,
        'revenue_day':revenue_day,
        'orders':orders,
        'monthly_total_prices':monthly_total_prices,
        'cod_count':cod_count,
        'razorpay_count':razorpay_count

    }
    return render(request,'c_admin/dashboard.html',context)
    
   
