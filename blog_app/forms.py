from django import forms
from froala_editor.widgets import FroalaEditor
from .models import BlogModel, Profile


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['content']

class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ['bio', 'profile_pic', 'facebook_url', 'instagram_url', 'linkedin_url', 'threads_url']      
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control col-md-6'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control col-md-6'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control col-md-6'}),
            'threads_url': forms.URLInput(attrs={'class': 'form-control col-md-6'}),
        }


