from django.contrib.auth.models import User
from django import forms
from .models import *
from pagedown.widgets import PagedownWidget
class PostForm(forms.ModelForm):
    publish=forms.DateField(widget=forms.SelectDateWidget)
    content=forms.CharField(widget=PagedownWidget(show_preview=False))


    class Meta:
        model=Post
        fields=['title','content','image','draft','publish',]
    def clean_title(self):
        title=self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title cannot be blank")
        return title
