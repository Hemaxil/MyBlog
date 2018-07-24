#from Blog.models import Post
#since importing comments from Comment in Post , we cannot import Post in Comments --do not func dually
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


# Create your models here.
#ModelManagers redefine the qs tools--like .all(),...
class CommentManager(models.Manager):
    def all(self):
        return super(CommentManager,self).filter(parent=None)

    def filter_by_instance(self,instance):
        #content_type=ContentType.objects.get_for_model(Post)
        content_type=ContentType.objects.get_for_model(instance.__class__)
        object_id=instance.id
        #super(CommentManager,self)--->Comment.objects
        return super(CommentManager,self).filter(content_type=content_type,object_id=object_id).filter(parent=None)
class Comment(models.Model):
    user        =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
    #post        =models.ForeignKey(Post,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment_text=models.TextField()
    timestamp   =models.DateTimeField(auto_now_add=True)
    parent= models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    objects=CommentManager()

    class Meta:
        ordering=['-timestamp']

    def __str__(self):
        return str(self.id)
    #replies to main comments
    def children(self):
        return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        return reverse("comments:thread",kwargs={"id":self.id},current_app='comments')

    def get_delete_url(self):
        return reverse("comments:comment_delete",kwargs={"id":self.id},current_app='comments')

    @property
    def is_parent(self):
        if self.parent!=null and self.parent is not None:
            return False
        else :
            return True
