from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *
from django import forms

# Create your models here.

class BlogModel(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    CATEGORIES = (('personal','PERSONAL'),
             ('Professional','PROFESSIONAL'),
             ('Niche','NICHE'),
             ('business','BUSINESS'),
             ('educational','EDUCATIONAL'),
             ('technology','TECHNOLOGY'),
             ('lifestyle','LIFESTYLE'),
             ('Review','REVIEW'),
             ('Creative','CREATIVE'),
             ('News','NEWS'),
             ('others','OTHERS'))
    categories = models.CharField(max_length=20, choices=CATEGORIES, null=True, default='others')
    content = FroalaField()
    slug = models.SlugField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def save(self, *args ,**kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save( *args ,**kwargs)



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(blank=True, null=True, max_length=500)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pic/')
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    instagram_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    threads_url = models.URLField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.user.username)
    
    def profile_image_url(self):
        """Return the uploaded image URL or a default image."""
        if self.image:
            return self.image.url
        return '/static/images/default_profile_pic.jpeg'



class ContactUs(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField()
    contact_no = models.CharField(max_length=12)
    feedback = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user.username)
    