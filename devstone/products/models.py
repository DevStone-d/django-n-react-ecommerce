from django.db import models

from django.utils.text import slugify

# Create your models here.

class Collection(models.Model):
    name            = models.CharField(max_length=100)
    img             = models.URLField()
    description     = models.TextField(null=True,blank=True)
    slug            = models.SlugField(unique=True,max_length=150,editable=False)
    meta_desc       = models.CharField(max_length=144,editable=False)

    def get_slug(self):
        slug = slugify(self.name)
        unique = slug
        number = 1
        while Collection.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1
        return unique

    def save(self,*args,**kwargs):
        if len(self.description) > 144:
            self.meta_desc = self.description[:144]
        else :
            self.meta_desc = self.description
        self.slug = self.get_slug()
        return super(Collection,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category        = models.ManyToManyField(Collection,related_name="category")
    name            = models.CharField(max_length=100)
    description     = models.TextField()
    video_url       = models.URLField(null=True, blank=True)
    slug            = models.SlugField(unique=True,max_length=150,editable=False)
    meta_desc       = models.CharField(max_length=144,editable=False)
    thumbnail       = models.URLField()
    is_active       = models.BooleanField(default=1)

    def get_slug(self):
        slug = slugify(self.name)
        unique = slug
        number = 1
        while Product.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1
        return unique

    def save(self,*args,**kwargs):
        if len(self.description) > 144:
            self.meta_desc = self.description[:144]
        else :
            self.meta_desc = self.description
        self.slug = self.get_slug()

        return super(Product,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class ProductDetail(models.Model):
    product         = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product")
    first_price     = models.FloatField(blank=True, null=True, default=-1) #optional, must be bigger/equal than/to price
    price           = models.FloatField()
    stock           = models.IntegerField()
    variant         = models.CharField(max_length=50,blank=True,default=-1)
    variable        = models.CharField(max_length=50,blank=True,default=-1)
    thumbnail       = models.URLField()

    def __str__(self):
        return f"{self.variable} {self.product.name}"


class ProductMedia(models.Model):
    product         = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_media")
    # image           = models.ImageField()
    image_url       = models.URLField()

    def __str__(self):
        return f"{self.image_url}"


class Tag(models.Model):
    product         = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="productdetail")
    tag             = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.product}-{self.tag}"