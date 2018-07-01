from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content','image',]
    def clean_title(self):
        title=self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title cannot be blank")
        return title
