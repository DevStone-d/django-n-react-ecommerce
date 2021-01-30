from django.db import models
from accounts.models import Account, Adress,Customer
from products.models import ProductDetail
from discounts.models import Coupon
from django.utils import timezone
# Create your models here.



class Cart(models.Model):
    customer                = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="buyer")
    ordered                 = models.BooleanField(default=0,editable=False)
    total                   = models.FloatField(editable=False,default=0.0)
    discounted              = models.FloatField(editable=False,default=0.0) ##
    coupon                  = models.CharField(max_length=50,blank=True,null=True)

    def customer_has_special_coupon(self):
        customer_coupon     = Coupon.objects.filter(customer=self.customer,code=self.coupon)
        if customer_coupon:
            return True
            
        else:
            return False

    def has_coupon(self):
        if self.coupon != None:
            coupon = Coupon.objects.filter(code=self.coupon) 
            if coupon:
                if coupon[0].customer is None:
                    return True
                return False
            else:
                return False
        else:
            return False

    def get_coupon(self):
        if self.customer_has_special_coupon():
            customer_coupon = Coupon.objects.filter(customer=self.customer,code=self.coupon)
            return customer_coupon[0]
        elif self.has_coupon():
            coupon = Coupon.objects.filter(code=self.coupon)
            return coupon[0]
        else:
            return None
        
    def get_total(self):
        total = 0.0
        items = OrderedItem.objects.filter(cart = self.id)
        for item in items:
            if item:
                total += item.total
        return total
    
    def is_valid(self):
        if self.total != self.get_total():
            return False
        else:
            return True

    def check_amount(self,req_amount):
        total = 0.0
        items = OrderedItem.objects.filter(cart = self.id)
        for i in items:
            total += i.total
        print("requested amount= ",req_amount)
        print("calculated total= ",total)
        print("self.amount= ",self.total) #self.amount du ama öyle bir field bile yok
        if (req_amount == total) and (self.total == req_amount) :
            return True
        return False

    def coupon_is_valid(self,coupon):
        if coupon.customer is not None:
            if (self.customer.id != coupon.customer.id):
                return False
            else:
                return True
        
        if coupon.coupon_type == '-1':
            return False
        elif coupon.coupon_type == '0' or coupon.coupon_type == '1':
            return True
        elif coupon.coupon_type == '2':
            if self.get_total() < coupon.above:
                return False
            else:
                return True
        elif coupon.coupon_type == '3':
            if self.get_total() < coupon.above:
                return False
            else:
                return True
        else:
            return False
            

    def get_discounted(self,coupon):
        if self.coupon_is_valid(coupon):
            if coupon.coupon_type == '0':
                self.discounted -= self.discounted/100*coupon.amount
            elif coupon.coupon_type == '1':
                self.discounted -= coupon.amount
            elif coupon.coupon_type == '2':
                self.discounted = self.discounted/100*coupon.amount
            elif coupon.coupon_type == '3':
                self.discounted -= coupon.amount

    def save(self, *args, **kwargs):
        self.total = self.get_total()
        self.discounted = self.total
        if self.has_coupon() or self.customer_has_special_coupon():
            coupon = self.get_coupon()
            if coupon:
                if self.total > 0:
                    self.get_discounted(coupon=coupon)
        else:
            self.coupon = None
        
        super().save(*args,**kwargs)

    def __str__(self):
        return self.customer.email + "'s Cart"

class OrderedItem(models.Model):
    cart            = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="orderedItems")
    item            = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,related_name="item")
    quantity        = models.IntegerField()
    total           = models.FloatField(blank=True,null=True,editable=False)

    def findTotal(self):
        return self.item.price * self.quantity
    
    def delete(self, *args, **kwargs):
        self.cart.save()
        super().delete(*args, **kwargs) 

    def save(self, *args, **kwargs):
        self.total = self.findTotal()
        super().save(*args,**kwargs)
        self.cart.save()
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
    def save(self, *args, **kwargs):
        if not self.id :
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args,**kwargs)
    def __str__(self):
        return f"Cart id: {self.id} Customer: {self.customer} "

