from django.urls import path
from . import views

urlpatterns = [
    path('admin_userlist/',views.admin_userlist,name='admin_userlist'),
    path('block_user/<int:user_id>',views.block_user,name='block_user'),
]
