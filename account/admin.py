from django.contrib import admin
from .models import Account


# Register your models here.


class acctAdmin(admin.ModelAdmin):
    list_display = ('profile', 'balance', 'active_investment', 'Total_earnings', 'last_deposit', 'date')


admin.site.register(Account, acctAdmin)