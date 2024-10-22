# A collection of video and audio processing tools

## Description
This repo performs various operations on video and audio files, including:
1. Extracting short video clips from longer ones.
2. Enhancing audio by adjusting pitch and volume, eg. for a deeper voice.
3. Extracting audio from a video and saving it as an MP3 file.
4. Amplifying audio if necessary.
5. Compressing and converting video files to WebM format.
6. Transcribing audio using Whisper.
7. Correcting raw audio transcripts using ChatGPT.
8. Embedding subtitles into the WebM video files.

## Main Functions
- Extract video clips.
- Enhance audio in a video file.
- Convert audio to MP3 and amplify it.
- Convert video to WebM format for web optimization.
- Transcribe audio using Whisper.
- Correct transcripts using AI (ChatGPT).
- Add subtitles to videos.

The main file of this repo is [runtools.py](runtools.py). In this file, 
(un)comment the functions you want execute.

## Requirements
- FFmpeg for video/audio processing. It must be installed on your machine and added to the PATH variable
- OpenAI API (Whisper and ChatGPT models) for transcription and transcript correction.
- Set OpenAI API key for ChatGPT in the [.env](.env) file. Whisper can be run without API key

## Info
* Latest update: 22 October 2024
* Author: Olaf Janssen (ookgezellig) - Supported by ChatGPT
* License: Creative Commons CC0 - http://creativecommons.org/publicdomain/zero/1.0
