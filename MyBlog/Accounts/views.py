from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,get_user_model,login,logout
from .forms import UserLoginForm,UserRegisterForm
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def login_view(request):
    action="Login"
    print(request.user.is_authenticated)
    form=UserLoginForm(request.POST)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        login(request,user)
        return HttpResponseRedirect("/")
    context={'form':form,'action':action}
    return render(request,'form.html',context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def register_view(request):
    action="Register"
    form=UserRegisterForm(request.POST)
    if form.is_valid():
        user=form.save(commit=False)
        user.set_password(form.cleaned_data.get("password"))
        user.save()
        return HttpResponseRedirect("/")
    context={'form':form,'action':action}
    return render(request,'form.html',context)
