from django.db import models
from accounts.models import UserProfile


# Create your models here.


class Wallet(models.Model):
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    