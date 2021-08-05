
from django.db import models
from rango.models import UserProfile
from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from rango.models import Page,Category,Comment

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH)
    description = forms.CharField(max_length=Category.DESCRIPTION_MAX_LENGTH)
    views = forms.IntegerField(widget=forms.HiddenInput,initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput,initial=0)
    slug = forms.CharField(widget=forms.HiddenInput,required=False)
    class Meta:
        model = Category
        fields = ('name','description','image',)

class PageForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH)
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) 
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    comments = forms.IntegerField(widget=forms.HiddenInput,initial=0)
    description = forms.CharField(widget=forms.Textarea,max_length=Page.DESCRIPTION_MAX_LENGTH)
    class Meta:
        model = Page
        fields = ('title','url','description','image',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email','password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website','picture',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea,max_length=Comment.CONTENT_MAX_LENGTH)
    
    class Meta:
        model = Comment
        fields = ('content',)