from django.db import models

# Create your models here.
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
# Create your models here.

class Post(models.Model):
    """docstring for .
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,default=1)"""
    title=models.CharField(max_length=100)
    #slug=models.SlugField(unique=True)
    #image=models.FileField(null=True,blank=True)
    #height_field=models.IntegerField(default=250)
    #width_field=models.IntegerField(default=250)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)

    def get_absolute_url(self):
        #return "/posts/details/%s" %(self.id)
        #never forget to add current_app, won't work without it
        return reverse("posts:details",kwargs={"id":self.id},current_app='Blog')
