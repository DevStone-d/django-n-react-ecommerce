from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Discount(models.Model):
    name                    = models.CharField(max_length=50)
    type_of_discount        = models.IntegerField()
    discount                = models.FloatField()
    created                 = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    valid_until             = models.DateTimeField(null=True,blank=True)
    is_valid                = models.BooleanField(default=True)

#class Admin(AbstractUser):
#    is_store = models.BooleanField(default=False)