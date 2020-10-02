from django.db import models

# Create your models here.


class Collection(models.Model):
    name            = models.CharField(max_length=100)
    img             = models.URLField()
    description     = models.TextField(null=True,blank=True)
    meta_url        = models.CharField(max_length=255)
    meta_desc       = models.CharField(max_length=144)


    def __str__(self):
        return self.name