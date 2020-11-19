from django.db import models
from accounts.models import Account, Adress
from products.models import ProductDetail
from discounts.models import Coupon
from django.utils import timezone

# Create your models here.

class Cart(models.Model):
    customer                = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="buyer")
    ordered                 = models.BooleanField(default=0,editable=False)
    total                   = models.FloatField(editable=False,default=0.0)
    discounted              = models.FloatField(editable=False,default=0.0) ##
    coupon                  = models.CharField(max_length=50,blank=True,null=True)

    def check_amount(self,req_amount):
        total = 0.0
        items = OrderedItem.object.filter(cart = self.id)
        for i in items:
            total += (i.item.price * i.item.quantity)
        print("requested amount= ",req_amount)
        print("calculated total= ",total)
        print("self.amount= ",self.amount)
        if (req_amount == total) and (self.amount == req_amount) :
            return True
        return False
    def __str__(self):
        return self.customer.first_name +" "+ self.customer.first_name + "'s Cart"
#sepetim'e gidilince quantity-> +1/-1 olabilir ya da quantity direkt guncellenebilir

class OrderedItem(models.Model):
    cart            = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="orderedItems")
    item            = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,related_name="item")
    quantity        = models.IntegerField()
    # item_total      = item.all.price()

    def __str__(self):
        return f"{self.cart.customer} added {self.item} to the cart : {self.cart.id}, id: {self.id}"

class Order(models.Model):
    STATUS_MEANS = [
        ('-1','Error'),
        ('0','Shopping'),
        ('1','Waiting for seller'),
        ('2','Payment Approved'),
        ('3','Order is preparing'),
        ('4','Shipped')
    ]
    cart                    = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="order")
    address                 = models.ForeignKey(Adress,on_delete=models.CASCADE,related_name="adress")
    created                 = models.DateTimeField(verbose_name='date created')
    modified                = models.DateTimeField(verbose_name='date modified')
    status                  = models.CharField(max_length=2,choices=STATUS_MEANS,default="0")
    amount                  = models.FloatField(editable=False,default=0.0)
    #discount                = models.ForeignKey(Discount,on_delete=models.CASCADE,related_name="indirim",blank=True,null=True)

    #customer                = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="buyer")
    #ordered                 = models.BooleanField(default=0,editable=False)
    # def check_amount(self,req_amount):
    #     total = 0.0
    #     items = OrderedItem.object.filter(cart = self.id)
    #     for i in items:
    #         total += (i.item.price * i.item.quantity)
    #     print("requested amount= ",req_amount)
    #     print("calculated total= ",total)
    #     print("self.amount= ",self.amount)
    #     if (req_amount == total) and (self.amount == req_amount) :
    #         return True
    #     return False
    def save(self, *args, **kwargs):
        if not self.id :
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args,**kwargs)
    def __str__(self):
        return f"Cart id: {self.id} Customer: {self.customer} "

