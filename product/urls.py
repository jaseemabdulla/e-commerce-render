from django.urls import path
from . import views

urlpatterns = [
    
    #brand
    path('admin_brand/',views.admin_brand,name='admin_brand'),
    path('add_brand/',views.add_brand,name='add_brand'),
    
    #category
    path('admin_category/',views.admin_category,name='admin_category'),
    path('add_category/',views.add_category,name='add_category'),
    
    #product
    path('product_list/',views.admin_product_list,name='admin_product_list'),
    path('add_product/',views.add_product,name='add_product'),
    path('variant_list/<int:product_id>/',views.admin_variant_list,name='admin_variant_list'),
    path('soft_delete_product/<int:variant_id>/',views.soft_delete_product,name='soft_delete_product'),
    path('edit_product_variant/<int:variant_id>/',views.edit_product_variant,name='edit_product_variant'),
    path('delete_variant_image/<int:image_id>/',views.delete_variant_image,name='delete_variant_image'),
    path('admin_variant_search/<int:product_id>/',views.admin_variant_search,name='admin_variant_search'),
    
    
    # =================================== user =================================== !
    
    # product
    path('shop/',views.user_product_list,name='user_product_list'),
    path('user_product_details/<int:product_id>/',views.user_product_details,name='user_product_details'),
    path('user_product_search/',views.user_product_search,name='user_product_search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    
]
