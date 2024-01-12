from django.shortcuts import render,redirect
from accounts.models import UserProfile

# Create your views here.


def admin_userlist(request):
    users = UserProfile.objects.all()
    
    return render(request,'c_admin/userlist.html',{'users':users})


def block_user(request,user_id):
    
    users = UserProfile.objects.all()
    user = UserProfile.objects.get(id = user_id)
    
    if user.is_superuser:
        return redirect('admin_login')
    
    if user.is_active:
        user.is_active = False
        user.save()
        
    else:
        user.is_active = True
        user.save()

    return render(request,'c_admin/userlist.html',{'users':users})