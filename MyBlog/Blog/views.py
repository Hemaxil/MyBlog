from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
from django.db.models import Q
from django import forms
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from urllib.parse import quote_plus


def post_list(request):
    ptitle="Latest Posts"
    queryset_list=Post.objects.active()
    if request.user.is_superuser:
        queryset_list=Post.objects.all()
    query=request.GET.get("q")
    if query:
        queryset_list=queryset_list.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(queryset_list,5) # Show 25 contacts per page
    page_var='abc'
    page = request.GET.get(page_var)
    queryset = paginator.get_page(page)
# to obtain 5 Latest posts
    context={
        'title':ptitle,
        'objlist':queryset,
        'page_var':page_var
        }
    return render(request,'base.html',context)
def post_create(request):
    if not (request.user.is_authenticated or request.user.is_superuser):
        raise Http404
    fname="Create Post"
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            print(request.user,instance.user)
            instance.save()
            #messages.success(request,"Successfully Created")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form=PostForm()

#messages.error(request,"Error in creating")
    context={'form':form,'fname':fname}
    return render(request,'createposts.html',context)

def post_update(request,slug):
    if not (request.user.is_superuser or request.user.is_authenticated):
        raise Http404
    fname="Update Post"
    queryset=get_object_or_404(Post,slug=slug)
    if not request.user.is_superuser:
        if queryset.user!=request.user:
            raise Http404
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES,instance=queryset)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(queryset.get_absolute_url())
    else:
        form=PostForm(instance=queryset)
    context={'instance':queryset,'form':form,'fname':fname,}
    return render(request,'createposts.html',context)

def post_detail(request,slug):
    if not (request.user.is_authenticated or request.user.is_superuser):
        raise Http404
    queryset=get_object_or_404(Post,slug=slug)
    share_content=quote_plus(queryset.content)
    share_title=quote_plus(queryset.title)
    print(queryset.get_content_type)
    initial_data={
    'content_type':queryset.get_content_type,
    'object_id':queryset.id,
    }
    comment_form=CommentForm(request.POST or None,initial=initial_data)
    print(comment_form.is_valid())
    if comment_form.is_valid():
        c_type=comment_form.cleaned_data.get("content_type")
        content_type=ContentType.objects.get(model=c_type)
        obj_id=comment_form.cleaned_data.get("object_id")
        comment_text=comment_form.cleaned_data.get("comment_text")
        try:
            parent_id=request.POST.get("parent_id")
        except:
            parent_id=null
        parent_obj=Comment.objects.get(id=parent_id)

        new_comment=Comment.objects.create(user=request.user,content_type=content_type,object_id=obj_id,
                                        comment_text=comment_text,parent=parent_obj)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    #content_type=ContentType.objects.get_for_model(Post)
    #object_id=queryset.id
    #comments=Comment.objects.filter_by_instance(queryset)
    comments=queryset.comments
    context={'obj':queryset,'sharecontent':share_content,'sharetitle':share_title,'comments':comments,'comment_form':comment_form}
    return render(request,'detail.html',context)

def post_delete(request,slug):
    if not (request.user.is_authenticated or request.user.is_superuser):
        raise Http404
    queryset=get_object_or_404(Post,slug=slug)
    if queryset.user!=request.user:
        raise Http404
    queryset.delete()
    return redirect('posts:lists')
