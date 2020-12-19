from django.db import models
from products.models import Collection,Product
# Create your models here.


class SiteMapItem(models.Model):
    ITEM_TYPES = [
        ('0','Yönlendirme'),
        ('1','Kategori'),
        ('2','Ürün'),
        ('3','Sayfa'),
    ]
    title                   = models.CharField(max_length=200)
    item_type               = models.CharField(max_length=2,choices=ITEM_TYPES,default="0")
    relationalModel         = models.CharField(max_length=100,null=True,blank=True)
    url                     = models.URLField(null=True,blank=True)
    haveChild               = models.BooleanField(default=False,editable=False)
    haveParent              = models.BooleanField(default=False,editable=False)
    
    def getCollection(self):
        try:
            collection = Collection.objects.get(slug=self.relationalModel)
        except:
            return ""
        return collection

    def getProduct(self):
        try:
            product = Product.objects.get(slug=self.relationalModel)
        except:
            return ""
        return product
    
    def save(self,*args,**kwargs):
        if self.item_type == "1":
            self.url = "/collections/"+self.getCollection().slug
        elif self.item_type == "2":
            self.url = "/products/"+self.getProduct().slug
        # elif self.item_type == "3":
        #     self.url = "/collections/"+self.getCollection().slug


        return super(SiteMapItem,self).save(*args,**kwargs)

    def __str__(self):
        return self.title
            

class SiteMap(models.Model):
    parentItem              = models.ForeignKey(SiteMapItem,on_delete=models.CASCADE,related_name="root")
    childItem               = models.ForeignKey(SiteMapItem,on_delete=models.CASCADE,related_name="child",null=True,blank=True)
    
    def save(self,*args,**kwargs):
        
        if self.childItem != None:
            item = SiteMapItem.objects.get(id=self.parentItem.id)
            item.haveChild = True
            item.save()
            item = SiteMapItem.objects.get(id=self.childItem.id)
            item.haveParent = True
            item.save()

        

    #     # elif self.item_type == "3":
    #     #     self.url = "/collections/"+self.getCollection().slug


        return super(SiteMap,self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.parentItem}  -  {self.childItem}"

class Categories(models.Model):
    parent                  = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name="parent")
    haveChild               = models.BooleanField(blank=True,null=True,editable=False)
    child                   = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name="childcollection",blank=True,null=True)

    def save(self,*args,**kwargs):
        if self.child != None :
            self.haveChild = True
        return super(Categories,self).save(*args,**kwargs)
    def __str__(self):
        return f"{self.parent}  -  {self.child}"