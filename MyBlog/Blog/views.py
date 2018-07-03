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
    fname="Create Post"
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            #messages.success(request,"Successfully Created")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form=PostForm()

#messages.error(request,"Error in creating")
    context={'form':form,'fname':fname}
    return render(request,'createposts.html',context)

def post_update(request,id):
    fname="Update Post"
    queryset=get_object_or_404(Post,id=id)
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES,instance=queryset)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(queryset.get_absolute_url())
    else:
        form=PostForm(instance=queryset)

    context={'instance':queryset,'form':form,'fname':fname,}
    return render(request,'createposts.html',context)

def post_detail(request,id):
    queryset=get_object_or_404(Post,id=id)
    context={'obj':queryset}
    return render(request,'detail.html',context)

def post_delete(request,id):
    queryset=get_object_or_404(Post,id=id)
    queryset.delete()
    return redirect('posts:lists')
