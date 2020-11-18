from django.db import models
from accounts.models import Account
from products.models import Product
from cart.models import Cart
# Create your models here.

class Coupon(models.Model):
    STATUS_MEANS = [
        ('-1','Error'),
        ('0','percentage'),
        ('1','direct'),
        ('2','directAbove'),
        ('3','percentageAbove'),
    ]
    customer = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="related user",blank=True, null=True)
    product  = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="related product",blank=True,null=True)
    cart     = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="related cart",blank=True, null=True)

    valid_until = models.DateTimeField()
    coupon_type = models.CharField(max_length=2,choices=STATUS_MEANS,default="0")
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.code + str(self.STATUS_MEANS[self.coupon_type])