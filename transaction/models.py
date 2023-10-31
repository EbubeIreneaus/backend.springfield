from django.db import models
from authentication.models import Profile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from account.models import Account
import time
from django.db import transaction
import datetime
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
    plan = models.CharField(max_length=12, choices=plans, null=True, blank=True)
    channel = models.CharField(max_length=9, choices=[('BTC', 'BTC'), ('USDT', 'USDT')],
                               default='BTC')
    type = models.CharField(max_length=9, choices=[('deposit','deposit'),('withdraw', 'withdraw')], default='deposit')
    amount = models.IntegerField()
    address = models.CharField(max_length=150, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)
    progress = models.CharField(max_length=12, choices=[('pending','pending'),('active','active'),
                                                        ('completed', 'completed')], default='pending')

    def __str__(self):
        return self.profile.user.first_name +" "+self.profile.user.last_name+" "+ str(self.amount)+' '+self.type+" "+\
            self.progress


def transaction_changed(instance_pk):
    try:
        with transaction.atomic():
            ts = Transaction.objects.select_for_update().get(pk=instance_pk)
            profile_id = ts.profile.pk
            account = Account.objects.select_for_update().get(profile__id=profile_id)
            now = datetime.datetime.now()
            tplan = {'bronze': 24, 'silver': 48, 'gold': 72, 'estate': 48, 'pro': 96}
            expires = datetime.datetime.fromtimestamp(time.time() + (60 * 60 * tplan[ts.plan]))
            if ts.status == 1:
                amount = ts.amount
                if ts.type == 'deposit':
                    ts.start_date = now
                    ts.end_date = expires
                    ts.progress = 'active'
                    account.active_investment = account.active_investment + amount
                    account.last_deposit = amount
                    ts.save()
                    account.save()
                else:
                    account.last_withdraw = amount
                    account.balance = account.balance + amount
                    ts.progress = 'completed'
                    account.save()
                    ts.save()
                print("success")
            else:
                ts.progress = 'completed'
                ts.save()
            return True

    except Exception as e:
        print(str(e))

@receiver(pre_save, sender=Transaction)
def transactionApprove(sender, instance,  **kwargs):
    try:
        sender.old_value = sender.objects.get(pk=instance.pk)

    except sender.DoesNotExist:
        pass


@receiver(post_save, sender=Transaction)
def transactionApprove(sender, instance, created, **kwargs):
    if not created:
        old_value = model_to_dict(sender.old_value)
        new_value = model_to_dict(instance)
        if old_value['status'] != new_value['status']:
            transaction_changed(instance.pk)

    else:
        pass