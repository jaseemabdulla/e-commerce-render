from django.urls import path
from . import views

urlpatterns = [
    path('offer_list/',views.offer_list,name='offer_list'),
    path('add_offer/',views.add_offer,name='add_offer'),
    path('apply_offer/',views.apply_offer,name='apply_offer'),
    path('remove_offer/<int:id>',views.remove_offer,name='remove_offer'),
    
]
