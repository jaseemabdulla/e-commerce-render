from django.urls import path
from . import views

urlpatterns = [
    path('user_signin/',views.user_signin,name='user_signin'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('login_with_otp/',views.login_with_otp,name='login_with_otp'),
    path('user_orders/',views.user_orders,name='user_orders'),
    path('user_address/',views.user_address,name='user_address'),
    path('user_details/',views.user_details,name='user_details'),
    path('user_orderdetails/<int:order_id>/',views.user_orderdetails,name='user_orderdetails'),
    path('user_cancel_order/<int:order_id>/',views.user_cancel_order,name='user_cancel_order'),
    
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),
    path('password-reset-invalid/', views.password_reset_invalid, name='password_reset_invalid'),

    path('download_invoice/<int:order_id>/', views.generate_invoice_pdf, name='download_invoice'),
   
    
    # admin 
    
    path('admin_login/',views.admin_login,name='admin_login'),
    
]
  