"""
Video and Audio Processing Module

====================================

Description:
This module performs various operations on video and audio files, including:
1. Extracting short video clips.
2. Enhancing audio by adjusting pitch and volume.
3. Extracting audio from a video and saving it as an MP3 file.
4. Amplifying audio if necessary.
5. Compressing and converting video files to WebM format.
6. Transcribing audio using Whisper.
7. Correcting raw audio transcripts using ChatGPT.
8. Embedding subtitles (both raw and AI-corrected) into the WebM video files.

Main Functions:
- Extract video clips.
- Enhance audio in a video file.
- Convert audio to MP3 and amplify it.
- Convert video to WebM format for web optimization.
- Transcribe audio using Whisper.
- Correct transcripts using AI (ChatGPT).
- Add subtitles to videos.

Requirements:
- FFmpeg for video/audio processing. It must be installed on your machine and added to the PATH variable
- OpenAI API (Whisper and ChatGPT models) for transcription and transcript correction.
- Set OpenAI API key for ChatGPT in the .env file. Whisper can be run without API key

Latest update: 22 October 2024
Author: Olaf Janssen (ookgezellig) - Supported by ChatGPT
License: Creative Commons CC0 - http://creativecommons.org/publicdomain/zero/1.0
"""

from tools import *
from transcribe_audio import transcribe_audio
from ai_correct_audiotranscripts import correct_transcript_file
from pathlib import Path

# Set up logging (optional)
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#== Directories and Files Definitions =======

# Input directory and file
input_dir = create_dir(Path('input_files'))
# input_file_name = 'WikidataWorkshop_MaastrichtUniversity_15October2024_TheoreticalPart.mp4'
input_file_name = 'WikidataWorkshop_MaastrichtUniversity_15October2024_PracticalPart_UMprofessors.mp4'
input_file = input_dir / input_file_name

# Output directories
output_dir = create_dir(Path('output_files'))  # Main output directory
video_dir = create_dir(output_dir / 'video')   # Video clips directory
webm_dir = create_dir(video_dir / 'webm')      # WebM clips directory
subtitled_video_dir = create_dir(webm_dir / 'subtitled')  # Subtitled video directory

# Audio directories
audio_dir = create_dir(output_dir / 'audio')   # Audio files directory
transcribed_audio_dir = create_dir(audio_dir / 'transcripts')  # Raw transcription files top level directory

# AI-corrected full text transcript and srt-subtitles directories
corrected_transcribed_txt_dir = create_dir(transcribed_audio_dir / 'corrected' / 'txt')  # ChatGPT-corrected audio txt transcripts
corrected_transcribed_srt_dir = create_dir(transcribed_audio_dir / 'corrected' / 'srt')  # ChatGPT-corrected audio srt subtitle files

#== Define Output File Paths =================
# Video file paths
input_stem = input_file.stem
input_suffix = input_file.suffix
video_clip_file = video_dir / f"{input_stem}-clipped{input_suffix}"  # Clipped file, for testing purposes
sound_enhanced_video_file = video_dir / f"{input_stem}-soundEnhanced{input_suffix}"  # Full sound-enhanced video
webm_video_file = webm_dir / f"{input_file.stem}.webm"  # WebM video file
subtitled_video_file = subtitled_video_dir / f"{input_file.stem}.webm"  # Subtitled WebM file

# Audio file paths
audio_file = audio_dir / f"{input_file.stem}.mp3"  # MP3 audio file
amplified_audio_file = audio_dir / f"{input_file.stem}-amplified.mp3"  # Amplified MP3 audio file

# Raw (uncorrected) transcript and subtitle files
raw_transcribed_txt_file = transcribed_audio_dir / 'raw' / 'txt' / f"{audio_file.stem}.txt"
raw_transcribed_srt_file = transcribed_audio_dir / 'raw' / 'srt' / f"{audio_file.stem}.srt"

# AI-corrected transcript and subtitle files
corrected_transcribed_txt_file = corrected_transcribed_txt_dir / f"{audio_file.stem}.txt"
corrected_transcribed_srt_file = corrected_transcribed_srt_dir / f"{audio_file.stem}.srt"

# Printing paths (optional, for debugging)
print(f"== Input file == ")
print(f" * Input file: {input_file}")
print(f"== Output files === ")
print(f"  === Video files == ")
print(f"   * Clipped video file: {video_clip_file}")
print(f"   * Sound enhanced video file: {sound_enhanced_video_file}")
print(f"   * WebM encoded and compressed video file: {webm_video_file}")
print(f"   * Subtitled video file: {subtitled_video_file}")
print(f"  === Extracted audio files == ")
print(f"   * Extracted audio file: {audio_file}")
print(f"   * Amplified extracted audio file: {amplified_audio_file}")
print(f"  === Raw audio transcription files == ")
print(f"   * Raw (uncorrected) transcript TXT file: {raw_transcribed_txt_file}")
print(f"   * Raw (uncorrected) transcript SRT file: {raw_transcribed_srt_file}")
print(f"  === AI/ChatGPT corrected transcription files == ")
print(f"   * AI/ChatGPT corrected transcript TXT file: {corrected_transcribed_txt_file}")
print(f"   * AI/ChatGPT corrected transcript SRT file: {corrected_transcribed_srt_file}")

#=================================
def main():
    try:
        # 1. Extract short clip for testing purposes (first 60 seconds)
        start_time = "00:00:00"  # Start from the beginning of the video
        duration = "00:01:00"    # 1 minute clip
        #extract_clip(input_video=input_file, start_time=start_time, duration=duration, output_clip=video_clip_file)  # Clipped part of source video

        # 2. Enhance the audio in the video and save the new video
        pitch_semitones = -1.2  # Lower the pitch by 1.2 semitones for a deeper voice
        db_increase = 0  # Increase the audio by 0dB
        #enhance_audio_in_video(input_video=input_file, output_video=sound_enhanced_video_file, pitch_semitones=pitch_semitones, db_increase=db_increase)

        # 3. Compress and convert the clip to WebM format
        #compress_and_convert_to_webm(input_clip=input_file, output_webm=webm_video_file)

        # 4. Extract the audio from the video clip and save as MP3
        #extract_audio(input_video=input_file, output_audio=audio_file)

        # 5. Amplify the audio if necessary
        amp_factor = 1.5  # Amplification factor
        #amplify_audio(input_audio=audio_file, output_audio=amplified_audio_file, factor=amp_factor)

        # 6. Transcribe the audio using Whisper and generate a .srt file
        whisper_model = "large-v2"
        #transcribe_audio(input_audio_path=audio_file, output_folder=transcribed_audio_dir, model_type=whisper_model)

        # 7. Correct the raw audio transcript using ChatGPT with a delay between chunks
        chatgpt_model = "gpt-4o"
        delay_between_chunks = 10  # 10-second delay between processing chunks
        #correct_transcript_file(input_file=raw_transcribed_txt_file, output_file=corrected_transcribed_txt_file, model=chatgpt_model, delay_between_chunks=delay_between_chunks)

        # 8. Add (raw or AI-corrected) subtitles to the WebM video file
        #add_subtitles_to_webm(input_video=webm_video_file, subtitle_file=corrected_transcribed_srt_file, output_video=subtitled_video_file)

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()