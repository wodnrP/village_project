from django.db import models
from user.models import CustomAbstractBaseUser
# Create your models here.

class Account(models.Model):
    plus_cash = models.IntegerField(null=True)
    minus_cash = models.IntegerField(null=True)
    total_cash = models.IntegerField(null=True)
    explain = models.CharField(max_length=100)
    memo = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    designate_date = models.DateField()
    admin_user = models.ForeignKey(CustomAbstractBaseUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.explain
