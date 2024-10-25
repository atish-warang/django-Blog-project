from django.contrib import admin
from .models import BlogModel, Profile

# Register your models here.

class BlogModalAdmin(admin.ModelAdmin):
    list_display = ['title','author','created_at','image']

admin.site.register(BlogModel, BlogModalAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','bio','profile_pic','facebook_url','instagram_url','linkedin_url','threads_url']

admin.site.register(Profile,ProfileAdmin)

