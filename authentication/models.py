from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your models here.
class Profile(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=17)
    country = models.CharField(max_length=40)
    verified = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name