from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import *
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import torch
from transformers import RobertaTokenizer
from django.conf import settings
import os
import numpy as np

import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from .utils import evaluate_submission
from .model.seq2seq_model import Seq2Seq 
from .model.run import convert_examples_to_features, Example,Args
import pandas as pd
from tqdm import tqdm

class CodeExplanationView():
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Get code from the request
        code = request.POST.get('code', '')

        
        # Use your Seq2Seq model to generate explanations
        explanation = self.generate_explanation(code)

        # Return the explanation as JSON response
        return JsonResponse({'explanation': explanation})

    
    @staticmethod
    def calculate_max_length(code, tokenizer):
        token_lengths = [len(tokenizer.tokenize(line)) for line in code.split('\n')]
        max_length = int(np.quantile(token_lengths, 0.95))
        return max_length 

    def get_preds(self,text, model, tokenizer, source_length, target_length):
        
        examples = [Example(0, source=text, target="")]  # Create a single Example instance with user input
        args = Args(source_length, target_length)  # Create Args instance with source_length and target_length
        eval_features = convert_examples_to_features(examples, tokenizer, args, stage='test')
        source_ids = torch.tensor(eval_features[0].source_ids, dtype=torch.long).unsqueeze(0)
        source_mask = torch.tensor(eval_features[0].source_mask, dtype=torch.long).unsqueeze(0)
        
        predictions = []
        with torch.no_grad():
            preds = model(source_ids=source_ids, source_mask=source_mask)
            
            for pred in preds:
                t = pred[0].cpu().numpy()
                t = list(t)
                if 0 in t:
                    t = t[:t.index(0)]
                text = tokenizer.decode(t, clean_up_tokenization_spaces=False)
                predictions.append(text)

        return predictions
    

    def generate_explanation(self, code):
        # Load the state dictionary
        model_state_dict = torch.load(settings.MODEL_PATH, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        # for key in model_state_dict.keys():
        #     print(key)
        tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
        # inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True)
        # Instantiate your custom Seq2Seq model
        max_length = CodeExplanationView.calculate_max_length(code, tokenizer)
        pretrained_model = 'microsoft/codebert-base'
        config = RobertaConfig.from_pretrained(pretrained_model)
        beam_size = 10
        # self.model = Seq2Seq(config)
        encoder = RobertaModel.from_pretrained(pretrained_model, config=config)
        decoder_layer = nn.TransformerDecoderLayer(d_model=config.hidden_size, nhead=config.num_attention_heads)
        decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)

        model = Seq2Seq(
            encoder=encoder,
            decoder=decoder,
            config=config,
            beam_size=beam_size,
            max_length=max_length,
            sos_id=tokenizer.cls_token_id,
            eos_id=tokenizer.sep_token_id
        )
        # Load the state dictionary into the model
        model.load_state_dict(model_state_dict)

        # Ensure the model is in evaluation mode
        model.eval()

        # Tokenize the input code
        

        # Move inputs to 'cuda' if available
        # for key in inputs:
        #     inputs[key] = inputs[key].to('cuda' if torch.cuda.is_available() else 'cpu')

        # # Perform a forward pass through the model
        # with torch.no_grad():
        #     print(inputs['input_ids'])
        #     outputs = model(inputs['input_ids'])
        #     print(outputs)
        source_length=256
        target_length=max_length
        
        predictions = self.get_preds(code, model, tokenizer, source_length, target_length)


        # Extract and return the explanation (modify based on your actual output format)
        # print(predictions)
        explanation = f"Explanation for code:\n{code}\n\nGenerated Explanation:{predictions}\n"

        return predictions


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
    var=CodeSnippet.objects.all().filter(language=language.strip())
    print(var)
    return render(request,'explore.html',{'var':var})
def explanation(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        
        # result=CodeExplanationView(code)
        # return render(request,'explanation.html',{'result':result})
        view = CodeExplanationView()
        response=view.post(request)
        predictions=json.loads(response.content.decode('utf-8'))
        return render(request,'explanation.html',{'predictions':predictions,'code':code})

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

def practice(request):
    problems=Problem.objects.all()
    # sub=Submission.objects.all().filter(user=request.user)
    return render(request,'practice.html',{'problems':problems})
# def problem_view(request,id):
#     problem=Problem.objects.all().filter(id=id)
    
#     return render(request,'problem.html',{'problem':problem})


def leaderboard(request):
    # Retrieve users along with the count of submissions by each user
    user_submission_counts = Submission.objects.values('user').filter(status='Accepted' , user__is_staff=False).annotate(total_submissions=Count('user'))

    # Retrieve user information for each user
    users = User.objects.filter(id__in=[entry['user'] for entry in user_submission_counts])
    print(user_submission_counts)
    # Combine user information with submission count
    leaderboard_data = [{'user': user, 'total_submissions': entry['total_submissions']} for user, entry in zip(users, user_submission_counts)]

    # Sort leaderboard data based on the number of submissions (descending order)
    leaderboard_data.sort(key=lambda x: x['total_submissions'], reverse=True)
    print(leaderboard_data)
    return render(request, 'leaderboard.html', {'leaderboard_data': leaderboard_data})


def submissions(request):
    submissions=Submission.objects.all().filter(user=request.user)
    print(submissions)
    return render(request,'submissions.html',{'submissions':submissions})

def challenge_detail(request, challenge_id):
    sub=Submission.objects.filter(challenge_id=challenge_id, user=request.user).order_by('-date').first()
    # print(sub.code)
    problem = Problem.objects.get(id=challenge_id)
    return render(request, 'problem.html', {'problem': problem,'challenge':challenge_id,'sub':sub})


@csrf_exempt
def compile_and_execute_code(code, language, inputs):
    url = 'http://localhost:5000/compile_and_execute'  # Replace with your compiler container's IP address

    data = {
        'code': code,
        'language': language,
        'inputs': inputs
    }

    response = requests.post(url, json=data)
    print(response.json())
    return response.json()




def compile_code(request,challenge_id):
    if request.method == 'POST':
        problem_id = challenge_id
        data = json.loads(request.body)
        
        # Extract code and language from the JSON data
        code = data.get('code')
        
        language =  data.get('lang')
        

        problem = Problem.objects.get(id =problem_id)
       
        test_cases = problem.test_cases.all()

        results = []
        for test_case in test_cases:
            test_input = test_case.input_data
            expected_output = test_case.expected_output
            print(language)
            result = compile_and_execute_code(code, language, test_input)
            print(result)
            print(test_input)
            result['input'] = test_input  # Include input in the result
            result['expected_output'] = expected_output
            results.append(result)
        # print(result)
        print(results)
        return JsonResponse({'results': results})
        # return redirect('/result/')



    problems = Problem.objects.all()
    return render(request, 'compile_and_execute.html', {'problems': problems})

def compile_submit(request,challenge_id):
    if request.method == 'POST':
        problem_id = challenge_id
        data = json.loads(request.body)
        
        # Extract code and language from the JSON data
        code = data.get('code')
        
        language =  data.get('lang')
        

        problem = Problem.objects.get(id =problem_id)
       
        test_cases = problem.test_cases.all()

        results = []
        status=''
        for test_case in test_cases:
            test_input = test_case.input_data
            expected_output = test_case.expected_output

            result = compile_and_execute_code(code, language, test_input)
            if result['error'].strip() != '':
                status = 'Compile Error'
            elif result['output'].strip() != expected_output.strip():
                status = 'Wrong Answer'
            else:
                status='Accepted'
            print(status)
            # print(result)
            result['input'] = test_input  # Include input in the result
            result['expected_output'] = expected_output
            results.append(result)
        # print(result)
        # print(results)
        var=Submission.objects.create(challenge=problem,user=request.user,code=code,status=status)
        print(var)
        return JsonResponse({'results': results})
        # return redirect('/result/')



    problems = Problem.objects.all()
    return render(request, 'compile_and_execute.html', {'problems': problems})


def result(request):
    return render(request,'practice.html')