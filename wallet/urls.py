from django.urls import path
from . import views

urlpatterns = [
    
    path('user_wallet/',views.user_wallet,name='user_wallet')
]
