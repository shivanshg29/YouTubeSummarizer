
# YouTube Transcript Summarizer

An interactive application built using Django REST Framework to summarize YouTube videos. This project uses `yt_dlp` to download `.webm` audio files, transcribes them with AssemblyAI, and summarizes the transcription using the Gemini API.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

---

## Introduction

This application processes YouTube video links to provide a concise summary. Here's how it works:
1. **Audio Extraction**: Uses `yt_dlp` to download the audio of a given YouTube video.
2. **Transcription**: Sends the audio to AssemblyAI for transcription.
3. **Summarization**: Feeds the transcription to the Gemini API to generate a professional summary.

The backend is powered by Django REST Framework, making the application easy to extend and scale.

---

## Features
- Download audio directly from YouTube.
- Automatic transcription using AssemblyAI.
- AI-generated summaries via Gemini API.
- RESTful API for integration with other applications.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up a `.env` file in the project root directory with the following content:
   ```env
   ASSEMBLY_API_KEY=your_assembly_ai_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

   Ensure to replace `your_assembly_ai_key` and `your_gemini_api_key` with your actual API keys.

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Configuration

This project uses `python-dotenv` to manage environment variables. To load the `.env` file, the following code snippet is used:

```python
from dotenv import load_dotenv
load_dotenv()
```

Ensure your `.env` file includes the required API keys:
- `ASSEMBLY_API_KEY`: API key for AssemblyAI.
- `GEMINI_API_KEY`: API key for the Gemini API.

---

## Usage

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Access the API endpoint to generate a summary:
   ```
   GET /api/get-summary?link=<YouTube URL>
   ```

   Replace `<YouTube URL>` with the link to the video you want summarized.

3. Example response:
   ```json
   {
       "content": "This is a professional summary of the video content."
   }
   ```

---

## Dependencies

The following Python packages are required for this project:
- `Django`
- `djangorestframework`
- `yt_dlp`
- `assemblyai`
- `python-dotenv`
- `google-generativeai`

Ensure all dependencies are installed via `requirements.txt`.

---

## Troubleshooting

1. **Invalid API Key Errors**:
   - Verify that `ASSEMBLY_API_KEY` and `GEMINI_API_KEY` are correctly set in the `.env` file.

2. **Issues with `yt_dlp`**:
   - Make sure `yt_dlp` is installed and up-to-date.
   - Check if the YouTube link is accessible and valid.

3. **File Permissions**:
   - Ensure the application has permission to create and delete files in the `MEDIA_ROOT` directory.

---

## Contributors

- [Your Name](https://github.com/your-username) - Creator and maintainer

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
