from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import yt_dlp
import assemblyai as aai
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os

load_dotenv()

# Download audio-only using yt-dlp
def download_audio(link):
    output_path = settings.MEDIA_ROOT
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Clean the output directory before starting the download
    for file_name in os.listdir(output_path):
        file_path = os.path.join(output_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'worst*', 
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_path = ydl.prepare_filename(info_dict)
            return audio_path
    except Exception as e:
        # If an error occurs, you can log or print the error message
        print(f"An error occurred: {e}")
        return None

# Get transcript from audio
def get_transcript(audio_path):
    aai.settings.api_key = os.getenv('ASSEMBLY_API_KEY')

    try:
        transcriber = aai.Transcriber()
        print("Getting Transcripts")
        transcript = transcriber.transcribe(audio_path)
        print("Got Transcripts")
    except (KeyError, json.JSONDecodeError):
        return Response({'error': 'Assembly AI API Issue'}, status=400)

    return transcript.text

# Use LLM API to generate summary
def generate_summary_llm(transcript):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f'{transcript} TASK: TL;DR/SUMMARY of TEXT in JSON. JSON keys: "titles" (array of strings): 2-5 appropriate titles for TEXT; "tags" (string): tag cloud; "entities" (array of {"name", "description"} objects): named entities, including persons, organizations, processes, etc. their detailed description and relationships; "short_summaries" (array of strings): one-two sentence summaries of TEXT; "style" (string): type, sentiment and writing style of TEXT; "arguments" (array of strings): 5-10 main arguments of TEXT; "summary" (string): detailed summary of TEXT; "Notes"(string):Detailed text for the video to study & analyse each & every point in detail Explain the concept in a precise & elaborated manner;'
    try:
        print("Generating Summary")
        response = model.generate_content(prompt)
        print("Generated Summary")
    except (KeyError, json.JSONDecodeError):
        return Response({'error': 'Gemini API Issue'}, status=400)
    return response.text

# Return summary as JSON
@api_view(['get'])
def get_summary(request):
    try:
        yt_link = request.query_params.get('link')
        if not yt_link:
            return Response({'error': 'YouTube link is required'}, status=400)
    except (KeyError, json.JSONDecodeError):
        return Response({'error': 'Invalid data sent'}, status=400)
    
    try:
        audio_path = download_audio(yt_link)
        transcript = get_transcript(audio_path)
        os.remove(audio_path)
        if not transcript:
            return Response({'error': "Failed to get transcript"}, status=500)
        summary = generate_summary_llm(transcript)
        if not summary:
            return Response({'error': "Failed to generate summary"}, status=500)
        return Response({'content': summary})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
