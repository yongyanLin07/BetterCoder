from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model): 
    NAME_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 500
    
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'profile_images',blank=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    class Meta: 
        verbose_name_plural = 'Categories'

    def __str__(self): 
        return self.name
        
class Page(models.Model): 
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    DESCRIPTION_MAX_LENGTH = 500

    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    title = models.CharField(max_length=TITLE_MAX_LENGTH) 
    url = models.URLField() 
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'profile_images',blank=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Page,self).save(*args,**kwargs)
    
    class Meta:
        verbose_name_plural = 'Pages'

    def __str__(self): 
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to = 'profile_images',blank=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    CONTENT_MAX_LENGTH = 200
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    time = models.DateField(auto_now=True) # update comment time directly
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    page = models.OneToOneField(Page,on_delete=models.CASCADE)

class Like(models.Model): # without registration in rango/admin.py
    time = models.DateField(auto_now=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    page = models.OneToOneField(Page,on_delete=models.CASCADE)

    def __str__(self):
        return self.page.title + "(liked by " + self.user.username + ")"

class Mark(models.Model):
    time = models.DateField(auto_now=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    page = models.OneToOneField(Page,on_delete=models.CASCADE)

    def __str__(self):
        return self.page.title + "(marked by " + self.user.username + ")"