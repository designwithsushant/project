from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Projects
from django.contrib.auth import login, authenticate, logout
import re
from django.views.decorators.cache import cache_control
# Create your views here.
def home(request):
    projects = Projects.objects.all()
    return render(request, "index.html", {'projects' : projects})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminpage(request):
    projects = Projects.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, "panel.html", {'projects' : projects})
        else:
            messages.warning(request, "Access Denied...")
            return redirect('/login')
    else:
        messages.error(request, "Please login first...")
        return redirect('/login')

def loginpage(request):
    return render(request, "login.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def projectspage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            projects = Projects.objects.all
            return render(request, 'projects.html', {'projects' : projects})
        else:
            messages.warning(request, 'Access Denied...')
            return redirect('/login')
    else:
        messages.warning(request, "Please login first...")
        return redirect('/login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_project(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                img = request.FILES.get("projectimage")
                title = request.POST.get("projecttitle")
                para = request.POST.get("projectparagraph")
                link = request.POST.get("projectreadmore")

                if img == "":
                    messages.error(request, 'No image is selected...')
                    return redirect('/administrator')

                elif title == "":
                    messages.error(request, 'Please insert title')
                    return redirect('/administrator')

                elif para == "":
                    messages.error(request, 'Please insert para')
                    return redirect('/administrator')

                elif link == "":
                    messages.error(request, 'Please insert link')
                    return redirect('/administrator')

                elif len(title) > 100:
                    messages.error(request, 'Please enter less than 100 characters')
                    return redirect('/administrator')

                elif len(para) > 255:
                    messages.error(request, 'Please enter less than 255 characters')
                    return redirect('/administrator')

                elif len(link) > 255:
                    messages.error(request, 'Please enter less than 255 characters')
                    return redirect('/administrator')

                else:
                    project = Projects.objects.create(image=img, title=title, para=para, link=link)
                    project.save()
                    messages.success(request, "Project successfully created....")
                    return redirect('/administrator')
            else:
                messages.warning(request, "Access Denied...")
                return redirect('/login')
        else:
            messages.error(request, "Please login to your account")
            return redirect('/login')
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginback(request):
    if request.method == "POST":
        loginusername = request.POST.get("loginusername")
        loginpassword = request.POST.get("loginpassword")
        password_reg = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*^]).{8,16}$';
        user_reg = r'^[a-z_][a-z0-9_]*$';
        if loginusername == '':
            messages.warning(request, "Username cannot be empty!!!")
            return redirect("/login")
        
        elif loginpassword == '':
            messages.warning(request, "Password cannot be empty!!!")
            return redirect("/login")
        
        elif not re.fullmatch(user_reg, loginusername):
            messages.warning(request, "Invalid format for username!!!")
            return redirect("/login")

        elif not re.fullmatch(password_reg, loginpassword):
            messages.warning(request, "Invalid format for password!!!")
            return redirect("/login")
        
        else:
            user = authenticate(request, username=loginusername, password=loginpassword)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully...")
                return redirect('/administrator')
            else:
                messages.error(request, 'Invalid credentials...')
                return redirect('/login')
    else: 
        return HttpResponse("404 site is not found")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Loggedout successfully...')
        return redirect('/login')
    else:
        messages.warning(request, 'You are already logged out...')
        return redirect('/login')