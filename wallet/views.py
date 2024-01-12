from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wallet.models import Wallet

# Create your views here.


@login_required(login_url='user_login')
def user_wallet(request):
    user = request.user
    wallet, created = Wallet.objects.get_or_create(user=user)
    if created: 
        wallet = created  # Assign wallet to the newly created wallet object
    return render(request, 'user/account/profile/wallet.html', {'wallet': wallet})