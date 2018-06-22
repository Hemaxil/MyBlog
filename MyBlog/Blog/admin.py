from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=('title','timestamp','updated')
    list_filter=('updated','title',)
    list_per_page=5
    list_editable=('title',)
    search_fields=['title','content']
    list_display_links=('updated',)
    class Meta:
        model=Post
admin.site.register(Post,PostAdmin)
