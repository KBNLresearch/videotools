"""
This module provides a set of utilities for processing videos and audio files using FFmpeg,
including functions for extracting clips, enhancing audio, amplifying audio, adding subtitles,
and converting videos to WebM format. The module also supports operations like creating output
directories and organizing processed files into structured folders.

Main functionalities:
- `extract_clip`: Extracts a specific segment from a video file based on start time and duration.
- `enhance_audio_in_video`: Enhances audio in a video file by applying pitch shifting and volume adjustment.
- `extract_audio`: Extracts the audio track from a video file and saves it as an audio file (e.g., MP3).
- `amplify_audio`: Amplifies the volume of an audio file by a given factor.
- `compress_and_convert_to_webm`: Compresses and converts MP4 video to WebM format for web-optimized video playback.
- `add_subtitles_to_video`: Embeds AI-corrected subtitles (SRT) into a video file, with options for toggling subtitles on/off.

This module is designed to work with various file formats, particularly MP4 for videos and SRT for subtitle files.
It also automates directory creation and file organization to streamline media processing workflows.

Functions:
- `create_dir`: Helper function to create directories.
- `extract_clip`: Extracts a clip from a video file.
- `enhance_audio_in_video`: Enhances audio in a video file without extracting the audio track.
- `extract_audio`: Extracts audio from a video file.
- `amplify_audio`: Amplifies audio in a file by a specified factor.
- `compress_and_convert_to_webm`: Compresses and converts a video to WebM format.
- `add_subtitles_to_video`: Adds subtitles to a video file.
- Directory and file path management: Handles the creation of directories and file paths for processed media.

Requirements:
- FFmpeg installed on the system and available in the system's PATH.
- The `subprocess` module for running FFmpeg commands.
- Python's `pathlib` for handling file and directory paths.

Latest update: 22 October 2024
Author: Olaf Janssen (ookgezellig) - Supported by ChatGPT
License: Creative Commons CC0 - http://creativecommons.org/publicdomain/zero/1.0
"""

import subprocess
from pathlib import Path
from typing import Union

# Helper function to create directories
def create_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def extract_clip(input_video: Union[str, Path], start_time: str, duration: str, output_clip: Union[str, Path]) -> None:
    """
    Extracts a clip from an MP4 video file, starting at a specific time and for a given duration.
    Args:
        input_video (Union[str, Path]): Path to the input video file (e.g., .mp4).
        start_time (str): Start time of the clip (format: 'HH:MM:SS' or seconds).
        duration (str): Duration of the clip (format: 'HH:MM:SS' or seconds).
        output_clip (Union[str, Path]): Path where the output clip will be saved.
    Returns:
        None
    Raises:
        FileNotFoundError: If the input video file does not exist.
        subprocess.CalledProcessError: If FFmpeg fails to execute.
    """
    input_video = Path(input_video)
    output_clip = Path(output_clip)

    # Check if the input file exists
    if not input_video.exists():
        raise FileNotFoundError(f"Input video file {input_video} does not exist.")

    command = [
        'ffmpeg',
        '-i', str(input_video),  # Input video file
        '-ss', start_time,  # Start time of the clip
        '-t', duration,  # Duration of the clip
        '-c', 'copy',  # Copy without re-encoding
        str(output_clip)  # Output video file
    ]

    try:
        # Run FFmpeg command to extract the clip
        subprocess.run(command, check=True)
        print(f"Clip extracted successfully to {output_clip}")
    except subprocess.CalledProcessError as e:
        print(f"Error during clip extraction: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def enhance_audio_in_video(input_video: Union[str, Path], output_video: Union[str, Path], pitch_semitones: float, db_increase: float) -> None:
    """
    Enhances the audio in an MP4 video by applying pitch shifting and volume adjustment without extracting the audio first.
    Args:
        input_video (Union[str, Path]): Path to the input MP4 video file.
        output_video (Union[str, Path]): Path to the output video file with enhanced audio.
        pitch_semitones (float): The number of semitones to shift the pitch. Positive values increase pitch, negative values decrease it.
        db_increase (float): The amount in dB by which to increase the audio volume.
    Returns:
        None
    Raises:
        FileNotFoundError: If the input video file does not exist.
        subprocess.CalledProcessError: If FFmpeg fails to execute the command.
    """
    input_video = Path(input_video)
    output_video = Path(output_video)

    # Check if the input file exists
    if not input_video.exists():
        raise FileNotFoundError(f"Input video file {input_video} does not exist.")

    command = [
        'ffmpeg',
        '-i', str(input_video),  # Input video file
        '-vcodec', 'copy',  # Copy the video stream without re-encoding
        # Apply audio filters: pitch shifting and volume increase
        '-af', f"asetrate=44100*{2**(pitch_semitones / 12)}, atempo=1/{2**(pitch_semitones / 12)}, volume={db_increase}dB",
        str(output_video)  # Output video file with enhanced audio
    ]

    try:
        # Run the FFmpeg command to enhance the audio in the video
        subprocess.run(command, check=True)
        print(f"Audio enhancement completed successfully for {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio enhancement: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def extract_audio(input_video: Union[str, Path], output_audio: Union[str, Path]) -> None:
    """
    Extracts audio from a video file and saves it as a separate audio file.
    Args:
        input_video (Union[str, Path]): Path to the input video file.
        output_audio (Union[str, Path]): Path to the output audio file (e.g., .mp3, .wav).
    Returns:
        None
    Raises:
        FileNotFoundError: If the input video file does not exist.
        subprocess.CalledProcessError: If FFmpeg fails to execute.
    """
    input_video = Path(input_video)
    output_audio = Path(output_audio)

    # Check if the input file exists
    if not input_video.exists():
        raise FileNotFoundError(f"Input video file {input_video} does not exist.")

    command = [
        'ffmpeg',
        '-i', str(input_video),  # Input video file
        '-q:a', '0',  # Highest quality for audio extraction
        '-map', 'a',  # Map the audio stream
        str(output_audio)  # Output audio file
    ]

    try:
        # Run FFmpeg command to extract audio
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully to {output_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio extraction: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def amplify_audio(input_audio: Union[str, Path], output_audio: Union[str, Path], factor: float) -> None:
    """
    Amplifies the audio volume by a specified factor and saves the result to an output file.
    Args:
        input_audio (Union[str, Path]): Path to the input audio file.
        output_audio (Union[str, Path]): Path where the output audio file with amplified sound will be saved.
        factor (float): The amplification factor (e.g., 1.5 for 150% louder).
    Returns:
        None
    Raises:
        FileNotFoundError: If the input audio file does not exist.
        subprocess.CalledProcessError: If FFmpeg fails to execute the command.
    """
    input_audio = Path(input_audio)
    output_audio = Path(output_audio)

    # Check if the input audio file exists
    if not input_audio.exists():
        raise FileNotFoundError(f"Input audio file {input_audio} does not exist.")

    command = [
        'ffmpeg',
        '-i', str(input_audio),  # Input audio file
        '-filter:a', f'volume={factor}',  # Apply volume amplification filter
        str(output_audio)  # Output audio file with amplified audio
    ]

    try:
        # Run FFmpeg command to amplify the audio
        subprocess.run(command, check=True)
        print(f"Audio amplification completed successfully: {output_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio amplification: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def compress_and_convert_to_webm(input_clip: Union[str, Path], output_webm: Union[str, Path]) -> None:
    """
    Compresses and converts an MP4 video clip to WebM format, reducing the file size
    while maintaining acceptable video quality.
    Args:
        input_clip (Union[str, Path]): Path to the input MP4 video file.
        output_webm (Union[str, Path]): Path where the output WebM file will be saved.
    Returns:
        None
    Raises:
        FileNotFoundError: If the input video file does not exist.
        subprocess.CalledProcessError: If FFmpeg fails to execute the command.
    """
    input_clip = Path(input_clip)
    output_webm = Path(output_webm)

    # Check if the input file exists
    if not input_clip.exists():
        raise FileNotFoundError(f"Input video file {input_clip} does not exist.")
    # These settings reduce the file size by 10x, while video image quality is still OK
    command = [
        'ffmpeg',  # Command starts here
        '-i', str(input_clip),  # Input file
        '-c:v', 'libvpx-vp9',  # Use VP9 codec
        '-b:v', '600K',  # Reduce the video bitrate to 600 Kbps for smaller size
        '-crf', '60',  # Set high CRF for better compression (lower quality)
        '-cpu-used', '8',  # Speed up the encoding with optimizations
        '-vf', 'scale=1280:720',  # Downscale the video resolution to 720p
        '-c:a', 'libopus',  # Use Opus codec for better audio compression
        '-b:a', '128k',  # Set audio bitrate to 128 Kbps
        str(output_webm)  # Output WebM file
    ]

    try:
        # Run the FFmpeg command to compress and convert the video to WebM
        subprocess.run(command, check=True)
        print(f"Compression and conversion completed successfully: {output_webm}")
    except subprocess.CalledProcessError as e:
        print(f"Error during compression and conversion: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def add_subtitles_to_webm(input_video: Union[str, Path], subtitle_file: Union[str, Path],
                          output_video: Union[str, Path]) -> None:
    """
    Embeds a WebVTT subtitle track into a WebM video and ensures the subtitles are set to display by default.

    Args:
        input_video (Union[str, Path]): The file path to the input WebM video.
        subtitle_file (Union[str, Path]): The file path to the subtitle file in WebVTT format.
        output_video (Union[str, Path]): The file path where the output WebM video with subtitles will be saved.

    Raises:
        FileNotFoundError: If the input video or subtitle file is missing.
        subprocess.CalledProcessError: If the FFmpeg command fails to execute.
    """

    input_video = Path(input_video)
    subtitle_file = Path(subtitle_file)
    output_video = Path(output_video)

    # Check if input video and subtitle file exist
    if not input_video.exists():
        raise FileNotFoundError(f"Input video file not found: {input_video}")

    if not subtitle_file.exists():
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_file}")

    # FFmpeg command to add WebVTT subtitles to the WebM video
    command = [
        'ffmpeg',
        '-i', str(input_video),  # Input video file
        '-i', str(subtitle_file),  # Input WebVTT subtitle file
        '-c:v', 'copy',  # Copy video stream without re-encoding
        '-c:a', 'copy',  # Copy audio stream without re-encoding
        '-c:s', 'webvtt',  # Use WebVTT codec for subtitles
        '-disposition:s:0', 'default',  # Set subtitles to display by default
        '-metadata:s:s:0', 'language=eng',  # Set language metadata (English by default)
        str(output_video)  # Output WebM video with embedded subtitles
    ]
    try:
        # Run FFmpeg command to add subtitles
        subprocess.run(command, check=True)
        print(f"Subtitles added successfully to: {output_video}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to embed subtitles into {output_video}. FFmpeg error: {e}")
        raise

    except Exception as e:
        print(f"An unexpected error occurred while processing: {e}")
        raise
