from django.urls import path
from . import views

urlpatterns = [
    path('cart_view/',views.cart_view,name='cart_view'),
    path('add_to_cart/<int:product_id>/<int:variant_id>/',views.add_to_cart,name='add_to_cart'),
    path('delete_cart_item/<int:cartitem_id>/',views.delete_cart_item,name='delete_cart_item'),
    path('increment_cart_item/<int:cartitem_id>/',views.increment_cart_item,name='increment_cart_item'),
    path('decrement_cart_item/<int:cartitem_id>/',views.decrement_cart_item,name='decrement_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('add_address/',views.add_address,name='add_address'),
    path('place_order/',views.place_order,name='place_order'),
    path('proceed_to_pay/',views.proceed_to_pay,name='proceed_to_pay'),
    # path('order_summary/',views.order_summary,name='order_summary'),
    path('rpay_order_summary/<int:order_id>/',views.rpay_order_summary,name='rpay_order_summary'),
    
    
    
    
    # =================== Admin ================
    
    path('admin_orderlist/',views.admin_orderlist,name='admin_orderlist'),
    path('admin_orderdetails/<int:order_id>',views.admin_orderdetails,name='admin_orderdetails'),
    path('admin_edit_orderstatus/<int:order_id>',views.admin_edit_orderstatus,name='admin_edit_orderstatus'),

    
]
  