from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from pytube import YouTube
from django.conf import settings
import assemblyai as aai
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os

load_dotenv()

# Create your views here.

# get yt title
def get_Title(link):
    yt=YouTube(link)
    title=yt.title
    return title

# download audio
def get_audio(link):
    yt=YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

# get transcript
def get_transcript(link):
    audio=get_audio(link)
    aai.settings.api_key=os.getenv('Assembly_API_KEY')

    transcriber=aai.Transcriber()
    transcript=transcriber.transcribe(audio)

    return transcript.text

# use LLM api generate summary
def generate_summary_llm(transcript):
    genai.configure(os.getenv('Gemini_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Based on the following transcript from a YouTube video, write a Summary, write it based on the transcript, but dont make it look like a youtube video, summarize the transcript :\n\n{transcript}\n"
    response = model.generate_content(prompt)
    print(response.text)

# return summary as json

@api_view(['POST'])
def get_summary(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            yt_link=data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        title=get_Title(yt_link)
        transcript=get_transcript(yt_link)
        if not transcript:
            return JsonResponse({'error': " Failed to get transcript"}, status=500)
        summary=get_summary(transcript)
        if not summary:
            return JsonResponse({'error': " Failed to generate blog article"}, status=500)
        
        return JsonResponse({'content':summary})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
        
        
