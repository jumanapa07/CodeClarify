from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import *
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import torch
from transformers import RobertaTokenizer
# class CodeExplanationView(View):
#     template_name = 'code_app/explanation.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     @csrf_exempt  # Use csrf_exempt for simplicity. You may want to implement CSRF protection based on your app's requirements.
#     def post(self, request, *args, **kwargs):
#         # Get code from the request
#         code = request.POST.get('code', '')

#         # Use your Seq2Seq model to generate explanations (replace with your actual logic)
#         explanation = self.generate_explanation(code)

#         # Return the explanation as JSON response
#         return JsonResponse({'explanation': explanation})

#     def generate_explanation(self, code):
#         # Load the pre-trained Seq2Seq model
#         model_path = '/models/model_weights.pth'
#         model = torch.load(model_path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

#         # Tokenize the input code
#         tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
#         inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True)

#         # Move inputs to 'cuda' if available
#         for key in inputs:
#             inputs[key] = inputs[key].to('cuda' if torch.cuda.is_available() else 'cpu')

#         # Perform a forward pass through the model
#         with torch.no_grad():
#             outputs = model(**inputs)

#         # Extract and return the explanation (modify based on your actual output format)
#         explanation = f"Explanation for code:\n{code}\n\nGenerated Explanation:\n{outputs}"

#         return explanation
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
    var=CodeSnippet.objects.all().values('language')
    return render(request,'homepage.html',{'var':var})

def explore(request):
    var=CodeSnippet.objects.all()
    return render(request,'explore.html',{'var':var})
def snippet_view(request,id):
    # ids=request.GET['id']
    var=CodeSnippet.objects.all().filter(id=id)
    return render(request,'snippet.html',{'var':var})
def language_snippet(request,language):
    var=CodeSnippet.objects.all().filter(language=language)
    return render(request,'explore.html',{'var':var})
def explanation(request):
    return render(request,'explanation.html')
def share(request):
    if request.method=='POST':
        print('ju')
        title=request.POST['title']
        description=request.POST['description']
        print(description)
        codesnippet=request.POST['code']
        print(codesnippet)
        language=request.POST['language']
        CodeSnippet.objects.create(user=request.user,title=title,description=description,code=codesnippet,language=language)
        return HttpResponseRedirect('/home/')
    else:
        return render(request,'share.html')
