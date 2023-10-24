from django.db import models
from authentication.models import Profile


# Create your models here.
class Transaction(models.Model):
    plans = [
        ('bronze','Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('estate', 'Real Estate'),
        ('pro', 'Trading Pro')
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    transact_id = models.CharField(max_length=50, unique=True)
    plan = models.CharField(max_length=12, choices=plans, null=True)
    channel = models.CharField(max_length=9, choices=[('BTC', 'BTC'), ('USDT', 'USDT')],
                               default='BTC')
    type = models.CharField(max_length=9, choices=[('deposit','Deposit'),('withdraw', 'withdraw')], default='deposit')
    amount = models.IntegerField()
    address = models.CharField(max_length=150, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    progress = models.CharField(max_length=12, choices=[('pending','pending'),('active','active'),
                                                        ('completed', 'completed')], default='pending')

    def __str__(self):
        return self.profile.user.first_name +" "+self.profile.user.last_name+" "+ str(self.amount)+' '+self.type+" "+\
            self.progress