from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from .models import Comment

def comment_delete(request,id):
    #obj=get_object_or_404(Comment,id=id)
    try:
        obj=Comment.objects.get(id=id)
    except:
        response=HttpResponse("This page does not exist")
        response.status_code=404
        return response
    if obj.user!=request.user:
        response=HttpResponse("You do not have permission to delete this Comment")
        response.status_code=403
        return response

    if request.method=='POST':
        post_url=obj.content_object.get_absolute_url()
        obj.delete()
        return HttpResponseRedirect(post_url)
    context={'obj':obj,}
    return render(request,'comment_delete.html',context)

def comment_thread(request,id):
    try:
        obj=Comment.objects.get(id=id)
    except:
        response=HttpResponse("This page does not exist")
        response.status_code=404
        return response
    #obj=get_object_or_404(Comment,id=id)
    print(obj.object_id)
    initial_data={
    'content_type':obj.content_type,
    'object_id':obj.object_id,
    }
    comment_form=CommentForm(request.POST or None,initial=initial_data)
    if comment_form.is_valid():
        c_type=comment_form.cleaned_data.get("content_type")
        content_type=ContentType.objects.get(model=c_type)
        obj_id=comment_form.cleaned_data.get("object_id")
        comment_text=comment_form.cleaned_data.get("comment_text")
        try:
            parent_id=request.POST.get("parent_id")
            parent_obj=Comment.objects.get(id=parent_id)
        except:
            parent_obj=None


        new_comment=Comment.objects.create(user=request.user,content_type=content_type,object_id=obj_id,
                                        comment_text=comment_text,parent=parent_obj)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context={'comment':obj,'comment_form':comment_form,}
    return render(request,'comment_thread.html',context)
