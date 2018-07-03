from django import forms
from django.contrib.auth import authenticate,get_user_model,login,logout


User=get_user_model()
class UserLoginForm(forms.Form):
    username=forms.CharField(max_length=50,label="Username")
    password=forms.CharField(widget=forms.PasswordInput,required=True,label="Password")
    ##email=forms.EmailField(label="Email Address",required=True)
    #emailc=forms.EmailField(label="Confirm Email",required=True)
    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("User doesnot exists")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("user is not active")
class UserRegisterForm(forms.ModelForm):
    confirm_email=forms.EmailField(label="Confirm Email")
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','password','email','confirm_email']

    def clean_confirm_email(self):
        email=self.cleaned_data.get("email")
        print(email)
        confirm_email=self.cleaned_data.get("confirm_email")
        print(confirm_email)
        if email != confirm_email:
            raise forms.ValidationError("Email and Confirm email fields don't match")
        email_qs=User.objects.filter(email=email)
        print(email_qs)
        if email_qs.exists():
            print('True')
            raise forms.ValidationError("Email already exists")
        #return super(UserRegisterForm,self).clean(*args,**kwargs)
        return confirm_email
