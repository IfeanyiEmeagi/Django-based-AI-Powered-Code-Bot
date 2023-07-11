from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Codes
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration

# Download the model and tokenizer to a local directory
saved_directory = "website/saved_model"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(saved_directory)
model = T5ForConditionalGeneration.from_pretrained(saved_directory).to(device)



#set the programming languages
language_list = ['cpp', 'csharp', 'css', 'go', 'html', 'javascript',  'php', 'python', 'ruby', 'typescript']
# Create your views here.
def home(request):

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        #check if lang was selected
        if lang == "Select Programming Language":
            messages.success(request, "Hey, you forgot to select the programming language...")
            return render(request, 'home.html', {"language_list": language_list, "code": code, "lang": lang })
        
        
        else:
            #openai key
            openai.api_key = "***************************"

            #instantiate openai model
            openai.Model.list()

            #make openai response
            try:

                inputs = tokenizer.encode(f"Respond with only code. Fix this {lang} language code: {code}", return_tensors="pt").to(device)
                outputs = model.generate(inputs, max_length=100)
                response = (tokenizer.decode(outputs[0], skip_special_tokens=True))
            
                #response = model.generate(f"{code}", max_length=1000)
                #response = openai.Completion.create(
                #    engine = "text-davinci-003",
                #    prompt= f"Respond with only code. Fix this {lang} language code: {code}",
                #    temperature = 0,
                #    max_tokens = 1000,
                #    top_p = 1.0,
                #    frequency_penalty = 0.0,
                #    presence_penalty = 0.0
                #)
                #response = (response['choices'][0]["text"])

                #Save to database
                record = Codes(question=code, code_response=response, language=lang, user=request.user)
                record.save()

                return render(request, 'home.html', {"language_list": language_list, "response": response, "lang": lang})
            except Exception as e:
                return render(request, 'home.html', {"language_list": language_list, "response": e, "lang": lang})
    else:   
        #render the home page if the request method is not post
        return render(request, 'home.html', {"language_list": language_list})


#create suggest page
def suggest(request):
    if request.method == "POST":
        message = request.POST['message']
        lang = request.POST['lang']

        #check if lang was selected
        if lang == "Select Programming Language":
            messages.success(request, "Hey, you forgot to select the programming language...")
            return render(request, 'suggest.html', {"language_list": language_list, "code": message, "lang": lang })
        
        else:
            #openai key
            openai.api_key = "**********"

            #instantiate openai model
            openai.Model.list()

            #make openai response
            try:
                response = openai.Completion.create(
                            engine = "text-davinci-003",
                            prompt= f"Respond with only code: {message}. Language: {lang}",
                            temperature = 0,
                            max_tokens = 1000,
                            top_p = 1.0,
                            frequency_penalty = 0.0,
                            presence_penalty = 0.0
                        )
                response = (response['choices'][0]["text"])

                  #Save to database
                record = Codes(question=message, code_response=response, language=lang, user=request.user)
                record.save()

                return render(request, 'suggest.html', {"language_list": language_list, "response": response, "lang": lang})
            except Exception as e:
                return render(request, 'suggest.html', {"language_list": language_list, "response": e, "lang": lang})
    else:   
        #render the home page if the request method is not post
        return render(request, 'suggest.html', {"language_list": language_list})


#create the login function
def login_user(request):
    #get the username and the password from the login form
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.success(request, "Sorry, an error occurred, kindly reconfirm your username and password")
            return redirect('home')
    else:
        return render(request, 'home.html', {})
    
#create the logout function
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

#Create the register function

def register_user(request):
    #first scenario - when the user has filled the form and click submit
    if request.method == "POST":
        form = SignUpForm(request.POST)
        #check if the form is valid
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #authenticate the user and login then in
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Thanks for registering, happy coding!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {"form": form})

#create code history function
def code_history(request):
    if request.user.is_authenticated:
        codes = Codes.objects.filter(user_id=request.user.id)
        return render(request, 'code_history.html', {'codes': codes})
    else:
        messages.success(request, "You must be logged in to view this page")
        return redirect('home')
    
def delete_history(request, history_id):
    history = Codes.objects.get(pk=history_id)
    history.delete()
    messages.success(request, "Deleted successfully...")
    return redirect('code_history')
