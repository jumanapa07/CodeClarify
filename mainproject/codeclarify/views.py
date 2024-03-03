from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .forms import RegistrationForm
def register_view(request):
    form=RegistrationForm()
    print(form)
    context={'form':form}

    return render(request,'register.html',context)


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']  # Assuming you want to use the first password field

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f"Welcome, {user.username}. Your account has been created.")
            return render(request,'homepage.html')  
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def loginn(request):
    
    if request.method=="POST":
        
        username=request.POST.get('name')
        password=request.POST.get('pswd')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("user present")
            login(request, user)
            return HttpResponseRedirect('/home')  # Redirect to your home page on successful login
        else:
            print("Invalid")
            error_message = "Invalid login credentials"  # You can customize the error message
            return render(request, 'login.html', {'messages': error_message})
    
    else:
        return render(request,'login.html')

def index(request):
    return render(request,'login.html')
def home(request):
    return render(request,'homepage.html')

def explore(request):
    return render(request,'explore.html')
def explanation(request):
    return render(request,'explanation.html')
    