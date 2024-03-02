from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}. Your account has been created.")
            return redirect('home')  # Change 'home' to your desired redirect URL
        else:
            messages.error(request, "Invalid registration details. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def loginn(request):
    
    if request.method=="POST":
        
        username=request.POST.get('name')
        password=request.POST.get('pswd')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')  # Redirect to your home page on successful login
        else:
            error_message = "Invalid login credentials"  # You can customize the error message
            return render(request, 'index.html', {'messages': error_message})
    

    return render(request,'index.html')

def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'homepage.html')

def explore(request):
    return render(request,'explore.html')
def explanation(request):
    return render(request,'explanation.html')
    