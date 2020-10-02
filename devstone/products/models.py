from django.db import models
from collection.models import Collection
# Create your models here.

class Product(models.Model):
    category        = models.ManyToManyField(Collection,related_name="category")
    name            = models.CharField(max_length=100)
    description     = models.TextField()
    video_url       = models.URLField(null=True, blank=True)
    meta_url        = models.CharField(max_length=100,default=" ", unique=True)

    def fillMeta(self):
        metaname        = str(self.name).casefold().replace(" ","-")
        self.meta_url   = metaname

        return self.meta_url

    def newMeta(self,newmeta):
        newmeta         = newmeta.strip().casefold().replace(" ","-")
        self.meta_url   = newmeta

        return self.meta_url

    def __str__(self):
        return self.name

class ProductDetail(models.Model):
    product         = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product")
    first_price     = models.FloatField(blank=True, null=True, default=-1) #optional, must be bigger/equal than/to price
    price           = models.FloatField()
    stock           = models.IntegerField()

    variant         = models.CharField(max_length=50,blank=True,default=-1)
    variable        = models.CharField(max_length=50,blank=True,default=-1)


    def __str__(self):
        return f"{self.variable} {self.product.name}"


class ProductMedia(models.Model):
    product         = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,related_name="product_media")
    # image           = models.ImageField()
    image_url       = models.URLField()

    def __str__(self):
        return f"{self.image_url}"
class Tag(models.Model):
    product         = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,related_name="productdetail")
    tag             = models.CharField(max_length=100)