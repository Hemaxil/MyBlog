from urllib.parse import quote_plus
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import *
from .forms import *

def post_list(request):
    title="Latest Posts"
    queryset_list=Post.objects.active()
    if request.user.is_superuser:
        queryset_list=Post.objects.all()
    paginator = Paginator(queryset_list,5) # Show 25 contacts per page
    page_var='abc'
    page = request.GET.get(page_var)
    queryset = paginator.get_page(page)
# to obtain 5 Latest posts
    context={
        'title':title,
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
    context={'obj':queryset,'sharecontent':share_content,'sharetitle':share_title,}
    return render(request,'detail.html',context)

def post_delete(request,slug):
    if not (request.user.is_authenticated or request.user.is_superuser):
        raise Http404
    queryset=get_object_or_404(Post,slug=slug)
    if queryset.user!=request.user:
        raise Http404
    queryset.delete()
    return redirect('posts:lists')
