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
    haveParent              = models.BooleanField(default=False,editable=False)
    parent                  = models.IntegerField(null=True,blank=True)
    priority                = models.IntegerField(default=-1)
    
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
    
    def gethaveParent(self):
        if self.parent != None:
            return 1
        return 0

    def rootSort(self):
        roots = SiteMapItem.objects.filter(haveParent=False).order_by("priority")
        print(roots)
        for root in roots:
            print("ROOT----->",root)
            if root.priority == self.priority:
                root.priority += 1
                root.save()

    def priortyChange(self):
        siblings = SiteMapItem.objects.filter(parent=self.parent).order_by("priority")
        for sibling in siblings:
            if sibling.priority == self.priority:
                sibling.priority += 1
                sibling.save()

    def save(self,*args,**kwargs):
        if self.item_type == "1":
            self.url = "/collections/"+self.getCollection().slug
        elif self.item_type == "2":
            self.url = "/products/"+self.getProduct().slug
        # elif self.item_type == "3":
        #     self.url = "/collections/"+self.getCollection().slug

        self.haveParent = self.gethaveParent()
        if self.haveParent == True:
            self.priortyChange()
        if self.haveParent == False:
            self.rootSort()
        return super(SiteMapItem,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

class Categories(models.Model):
    parent                  = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name="parent")
    haveChild               = models.BooleanField(blank=True,null=True,editable=False)
    child                   = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name="childcollection",blank=True,null=True)

    def save(self,*args,**kwargs):
        if self.child != None : #child'ı boş değilse
            self.haveChild = True
        return super(Categories,self).save(*args,**kwargs)
    def __str__(self):
        return f"{self.parent}  -  {self.child}"