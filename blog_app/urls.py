from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact-us/', contact_us, name='contact_us'),
    path('about/', about, name='about'),

    path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),

    path('blog/', blog, name='blog'),
    path('blog-details/<slug>/', blog_details, name='blog_details'),
    path('create-blog/', create_blog, name='create_blog'),

    path('profile/', profile, name='profile'),
    path('user-profile/<str:user_id>/', user_profile, name='user_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-user/', delete_user, name='delete_user'),
    path('blog/delete/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('search/', search_view, name='search'),

    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password-change-done/', CustomPasswordChangeView.as_view(), name='password_change_done'),
]