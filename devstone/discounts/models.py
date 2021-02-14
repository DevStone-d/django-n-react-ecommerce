from django.db import models
from accounts.models import Customer
from products.models import Product
# Create your models here.

class Coupon(models.Model):
    STATUS_MEANS = [
        ('-1','Error'),
        ('0','percentage'),
        ('1','direct'),
        ('2','directAbove'),
        ('3','percentageAbove'),

        # ('4','userBasedDirect'),
        # ('5','userBasedDirectAbove'),  -LIMITED = 1
        # ('6','userBasedPer'),
        # ('7','userBasedPerAbove'),
    ]
    customer    = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="related_user",blank=True, null=True)
    valid_until = models.DateTimeField()
    coupon_type = models.CharField(max_length=2,choices=STATUS_MEANS,default="0")
    amount      = models.IntegerField()
    above       = models.IntegerField(blank=True,null=True)
    code        = models.CharField(max_length=50)
    is_active   = models.BooleanField()
    limited     = models.IntegerField()

    def __str__(self):
        return self.code