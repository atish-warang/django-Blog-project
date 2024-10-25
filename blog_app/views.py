from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import BlogModel,Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import * 

# Create your views here.

def home(request):
    return render(request, 'home.html')


def user_register(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if(email == '' or username == '' or password == '' or cpassword == ''): # To ensure all fields are filled
            context['error_msg'] = 'Please fill all fields !'
        
        elif(password != cpassword): # To check if password is matching with confirm password
            context['error_msg'] = 'password does not match with confirm password !'

        elif(User.objects.filter(username = username).exists()):# To check if user already exists whit the same username 
            context['error_msg'] = username + ' username already taken, try another one !'

        else:
            user = User.objects.create(username=username, email=email)# to create new user
            user.set_password(password)# To encrypt the password
            user.save()
            return redirect('/login')

    return render(request, 'register.html', context)



def user_login(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin')
        else:
            return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if (email == '' or username == '' or password == ''):
            context['error_msg'] = "please fill all fields !"

        # elif(not User.objects.filter(email=email).exists()):
        #     context['error_msg'] = 'Invalid E-mail !'

        elif( not User.objects.filter(username=username).exists()):
            context['error_msg'] = "Username " + username + " Does not Exists !"

        else:
            user = authenticate(email=email, username=username, password=password)

            if user is None:
                context['error_msg'] = "Invalid Password !"
            else:
                login(request, user)

                if user.is_superuser:
                    return redirect('/admin')
                else:
                    return redirect("/blog")        
    return render(request, 'login.html', context)



def user_logout(request):
    logout(request)
    return redirect('/')



def blog(request):
    all_blogs = BlogModel.objects.all()
    context = {'blogs': all_blogs}
    #print(context)
    return render(request, 'blog.html', context)



def blog_details(request, slug):
    all_blogs = BlogModel.objects.filter(slug = slug) 
    context = {'blogs': all_blogs}
    return render(request, 'blog_details.html', context)



def create_blog(request):
    context = {'form' : BlogForm}
    
    if request.method == 'POST':
        form = BlogForm(request.POST)
        image = request.FILES['image']
        title = request.POST.get('title')
        categories = request.POST.get('categories')
        author = request.user

        if form.is_valid():
            content = form.cleaned_data['content']

            BlogModel.objects.create(
            author = author,
            title = title,
            categories = categories,
            content = content,
            image = image
            )
            return redirect('/blog')
    return render(request, 'create_blog.html', context)




def profile(request):
    personal_blog = BlogModel.objects.all()
    context = {'personal_blog' : personal_blog}
    return render(request, 'profile.html', context)



def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    personal_blog = BlogModel.objects.all()
    context = {'personal_blog' : personal_blog, 'user': user}
    return render(request, 'view_profile.html', context)



def edit_profile(request):
    try:
        profile = request.user.profile  # Try to access the profile
    except Profile.DoesNotExist:
        # If profile doesn't exist, create one for the user
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})




class CustomPasswordChangeView(PasswordChangeView):   
    template_name = 'change_password.html'  # Your custom template
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been successfully changed! Logout and try login again with new password')
        return super().form_valid(form)
    


from django.db.models import Q

def search_view(request):
    query = request.GET.get('query', '')  # Get the query from the GET parameters
    blogs = BlogModel.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(categories__icontains=query)
    ) if query else BlogModel.objects.all()  # Show all blogs if no query

    return render(request, 'blog.html', {'query': query, 'blogs': blogs})



# def blog_list(request):
#     # Get the sorting parameter from GET request
#     sort_by = request.GET.get('sort', '-created_at')  # Default to sorting by created_at in descending order

#     # Ensure the sort_by is safe
#     sort_fields = ['created_at', 'title']
#     if sort_by not in sort_fields and sort_by != '-created_at':
#         sort_by = '-created_at'  # Fallback to default if invalid sort_by

#     # Get all blog posts sorted by the selected field
#     all_blogs = BlogModel.objects.all().order_by(sort_by)
    
#     context = {'blogs': all_blogs}
#     return render(request, 'blog.html', context)


def delete_user(request):
    user = request.user  # Get the currently logged-in user
    try:
        # Delete the associated profile if it exists
        profile = user.profile
        profile.delete()
    except Profile.DoesNotExist:
        pass  # If the profile doesn't exist, continue

    # Log out the user before deleting the user account
    logout(request)
    user.delete()  # Delete the user account

    return redirect('/')  # Redirect to homepage after deletion



def delete_blog(request, blog_id):
    blog = get_object_or_404(BlogModel, id=blog_id)

    if request.method == 'POST':
        if blog.author == request.user:  # Ensure the user is the author
            blog.delete()
            messages.success(request, "Blog deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete this blog.")

    return redirect('/profile')  # Redirect to the profile  page after deletion


def contact_us(request):
    return render(request, 'contact_us.html')



def about(request):
    return render(request, 'about.html')



























# def delete_profile(request):
#     profile = get_object_or_404(Profile, user=request.user)
#     profile.delete()
#     messages.success(request, 'Profile deleted successfully.')
#     return redirect('/')


# def edit_profile(request):
#     profile = get_object_or_404(Profile, user=request.user) 
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)  # Include request.FILES
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('/profile')  # Redirect to a profile page or a success page
#     else:
#         form = ProfileForm(instance=profile)
    
#     return render(request, 'edit_profile.html', {'form': form})