from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_extempt
from django.http import JsonResponse
import json

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')
@csrf_extempt
def generate_blog(request):
    if request.method =='POST':
        try:
            data= json.loads(request.body)
            yt_link=data['link']
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'Invalid data sent'}, status=400)
        #get yt title
        # get transcript
        #use open ai to generate the blog
        # save blog article to database
        # return blog article as a response     
    else:
        return JsonResponse({'error':'Invalid request method'}, status=405)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message= "Invalid username or password"
            return render (request, 'login.html',{'error message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            try:
                user= User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message= 'Error creating account'
                return render(request,'signup.html',{'error_message': error_message})
        else:
            error_message ='Passwords do not match'
            return render(request,'signup.html',{'error_message': error_message})
        
    return render(request, 'signup.html')    
def user_logout(request):
    logout(request)
    return redirect('/')         