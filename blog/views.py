from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post
from .forms import SignUpFrom, LoginFrom, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

## HOME VIEW
def home(request):
    dt = Post.objects.all()
    context = {
        'snapshots': dt,
        'home':'active',
        }
    return render(request, 'blog/home.html', context)

## ABOUT VIEW
def about(request):
    context = {
        'about':'active',
        }
    return render(request, 'blog/about.html', context)

## CONTACT VIEW
def contact(request):
    context = {
        'contact':'active',
        }
    return render(request, 'blog/contact.html', context)

## DASHBOARD VIEW
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        fullName = user.get_full_name()
        grps = user.groups.all()
        context = {
        'dashboard':'active',
        'posts':posts,
        'fullName':fullName,
        'groups':grps,
        }
        return render(request, 'blog/dashboard.html', context)
    else:
        return HttpResponseRedirect('/login/')
    


## SIGNUP VIEW
def user_signup(request):
    if request.method == 'POST':
        form = SignUpFrom(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            messages.success(request, 'Account Created')
        else:
            messages.error(request, 'Please try again')
    else:
        form = SignUpFrom()
    return render(request, 'blog/signup.html', {'form':form, 'signup':'active'})

## LOGIN VIEW
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginFrom(request=request, data = request.POST)
            if form.is_valid():
                userName = form.cleaned_data['username']
                password = form.cleaned_data['password']
                auth = authenticate(username=userName, password=password)
                if auth is not None:
                    login(request, auth)
                    messages.success(request, 'Login Successful')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginFrom()
        return render(request, 'blog/login.html', {'form':form, 'login':'active'})
    else:
        return HttpResponseRedirect('/dashboard/')

## LOGOUT VIEW
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

## ADD NEW POST
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                post = Post(title=title, desc=desc)
                post.save()
                # form = PostForm()
                # messages.success(request, 'Success!') 
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()     
        return render(request, 'blog/add_post.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
        
## UPDATE POST
def update_post(request, id, name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            dt = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=dt)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            dt = Post.objects.get(pk=id)
            form = PostForm(instance=dt)
        return render(request, 'blog/update_post.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
## DELETE POST
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            dt = Post.objects.get(pk=id)
            dt.delete()
            return HttpResponseRedirect('/dashboard/')
        else:
            return HttpResponse("YOU ARE NOT AUTHORIZED")
    else:
        return HttpResponseRedirect('/login/')