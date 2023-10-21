from django.db import models
from authentication.models import Profile

# Create your models here.
class Account(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    active_investment = models.IntegerField(default=0)
    pending_withdraw = models.IntegerField(default=0)
    Total_earnings = models.IntegerField(default=0)
    last_deposit = models.IntegerField(default=0)
    last_withdraw = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    
