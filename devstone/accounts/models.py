from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
from products.models import ProductDetail

class MyAccountManager(BaseUserManager):
    ##TOKEN VERİLECEK
    def create_user(self,email,first_name,last_name,password):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have an first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not password:
            raise ValueError("Users must have an password")

        user = self.model(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email ,first_name,last_name , password):
        user = self.create_user(email=self.normalize_email(email),password=password,first_name= first_name,last_name = last_name,)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_store = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
		

class Account(AbstractBaseUser):
    username = None
    email					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name              = models.CharField(max_length=200)
    last_name               = models.CharField(max_length=200)
    phone                   = models.CharField(verbose_name="phone",max_length=30,blank=True,null=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    date_of_birth           = models.DateField(verbose_name='birth date',blank=True,null=True)
    """
        Gender : 
            -1: Belirtmek istemiyorum
            0 : Erkek
            1 : K 
    """
    gender                  = models.IntegerField(blank=True,null=True,default=-1)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_superuser            = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False) #-1,0-1-2-3 staff perm, different perms
    is_store                = models.BooleanField(default=False)
    is_customer             = models.BooleanField(default=False)
    is_bakery               = models.BooleanField(default=False)
    is_delivery             = models.BooleanField(default=False)
    is_burhan               = models.BooleanField(default=False)
    is_editor               = models.BooleanField(default=False)
    is_accounting           = models.BooleanField(default=False)
    is_customerservice      = models.BooleanField(default=False)
    date_activate           = models.DateField(verbose_name="date of activate",blank = True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['first_name','last_name']
    objects = MyAccountManager()

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

class Adress(models.Model):
    user                    = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="customer")
    adress_first_name       = models.CharField(max_length=100)
    adress_last_name        = models.CharField(max_length=100)
    adress_phone            = models.CharField(verbose_name="phone",max_length=30)
    city                    = models.CharField(max_length=100)
    country                 = models.CharField(max_length=100)
    adresss                 = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.adress_first_name} {self.adress_last_name} - {self.adresss} {self.city}/{self.country}"
    

class Cart(models.Model):
    customer                = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="buyer")
    ordered                 = models.BooleanField(default=0,editable=False)
    total                   = models.FloatField(editable=False,default=0.0)
    #discount                = models.ForeignKey(Discount,on_delete=models.CASCADE,related_name="indirim",blank=True,null=True)

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
#sepetim'e gidilince quantity-> +1/-1 olabilir ya da quantity direkt guncellenebilir

class OrderedItem(models.Model):
    cart            = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="orderedItems")
    item            = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,related_name="item")
    quantity        = models.IntegerField()

    def __str__(self):
        return f"{self.cart.customer} added {self.item} to the cart : {self.cart.id}"

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
    created                 = models.DateTimeField(verbose_name='date created', auto_now_add=True)
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

    def __str__(self):
        return f"Cart id: {self.id} Customer: {self.customer} "

