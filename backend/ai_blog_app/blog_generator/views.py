from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from pytube import YouTube
import os
import assemblyai as aai
import openai 
# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')
@csrf_exempt
def generate_blog(request):
    if request.method =='POST': #when POST method is used csrf is important
        try:
            data= json.loads(request.body)
            yt_link= data['link']
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'Invalid data sent'}, status=500)
        #get yt title
        title= yt_title(yt_link)
        # get transcript
        transcription=get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error':'Failed to get transcript'}, status=500)
def yt_title(link):
    yt= YouTube(link)
    title= yt.title
    return title
def download_audio(link):
    yt=YouTube(link)
    video=yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext= os.path.splittext(out_file)
    new_file= base + '.mp3'
    os.rename(out_file, new_file)
def get_transcription(link):
    audio_file= download_audio(link)
    aai.settings.api_key= "abffd2ec232e47b88ea0d8bcdcfce6e9"

    transcriber= aai.Transcriber()
    transcript = transcriber.transcribe()
    return transcript.text
def generate_blog_from_transcription(transcription):
    openai.api_key = "sk-proj-..."  # your key

    prompt = (
        f"Based on the following transcript from a YouTube video, write a comprehensive blog article. "
        f"Write it based on the transcript, but format it like a proper blog post:\n\n{transcription}\n\nArticle:"
    )

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1000
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("🔥 OpenAI error:", e)  # ✅ This will show in your terminal
        return None


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