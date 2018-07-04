from django.db import models

# Create your models here.
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
# Create your models here.
def upload_location(intsance,filename):
    return "{0}/{1}".format(intsance.id,filename)
# to check whether the slug has been created or not
def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs_slug=Post.objects.filter(slug=slug).order_by('-id')
    exists=qs_slug.exists()
    if exists:
        #print(qs_slug.first().id)
        new_slug="%s-%s" %(slug,qs_slug.first().id)
        #print(new_slug)
        return create_slug(instance,new_slug)
    return slug

def pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

class Post(models.Model):
    """docstring for .
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,default=1)"""
    title=models.CharField(max_length=100,blank=True,null=True)
    slug=models.SlugField(unique=True)
    image=models.ImageField(upload_to=upload_location,height_field='height_field',width_field='width_field',null=True,blank=True)
    height_field=models.IntegerField(default=50)
    width_field=models.IntegerField(default=50)
    content=models.TextField(blank=True)
    timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return "/posts/details/%s" %(self.id)
        #never forget to add current_app, won't work without it
        return reverse("posts:details",kwargs={"slug":self.slug},current_app='Blog')
pre_save.connect(pre_save_receiver,sender=Post)
