"""
Whisper Audio File Transcription Script

=====================
Description:
This script processes audio files using the OpenAI Whisper model for automatic transcription.
It transcribes selected audio files from a specified directory and saves the results in multiple formats (`tsv`, `txt`, and `srt`).

Features:
- Transcription functionality using the OpenAI Whisper model.
- Saving transcription results in different file formats.
- Error handling for both transcription and file-saving operations.
- Adjustable selection of files for transcription.

Requirements:
- The Whisper package (https://github.com/openai/whisper)
- FFMPEG installed and included in the system's PATH variable (for Windows).

Latest update: 22 October 2024
Author: Olaf Janssen (ookgezellig) - Supported by ChatGPT
License: Creative Commons CC0 - http://creativecommons.org/publicdomain/zero/1.0
"""

import whisper
from whisper.utils import get_writer
from pathlib import Path
from typing import Dict, Optional

def transcribe_audio(input_audio_path: Path, output_folder: Path, model_type: str, language: str = 'en', verbose: bool = True) -> None:
    """
    Transcribes an audio file using the Whisper model and saves the results in multiple formats.
    Args:
        input_audio_path (Path): Path to the input audio file to be transcribed.
        output_folder (Path): The main folder where the transcript files will be stored.
        model_type (str): The Whisper ASR model ('large-v2' etc. )
        language (str): Language code for the transcription. Default is 'en'.
        verbose (bool): If True, print status updates and results to the console. Default is True.
    Returns:
        None
    Raises:
        FileNotFoundError: If the input audio file is not found.
        Exception: For any other errors encountered during transcription.
    """

    # Load the Whisper model
    model = whisper.load_model(model_type)

    input_audio_path = Path(input_audio_path)

    # Check if the input file exists
    if not input_audio_path.exists():
        raise FileNotFoundError(f"Input audio file {input_audio_path} does not exist.")

    try:
        if verbose:
            print(f"Transcribing {input_audio_path}...")

        # Transcribe the audio file
        result = model.transcribe(audio=str(input_audio_path), language=language, verbose=verbose)

        if result and 'text' in result:
            if verbose:
                print('-' * 50)
                print(result.get('text', ''))

            # Save the transcription in different formats
            for fmt in ['tsv', 'txt', 'srt']:
                save_transcription(result, input_audio_path, output_folder, fmt, verbose)
        else:
            if verbose:
                print(f"No transcription result for {input_audio_path}.")
    except Exception as e:
        print(f"An unexpected error occurred while transcribing {input_audio_path}: {e}")


def save_transcription(results: Dict[str, Optional[str]], inputfile: Path, output_folder: Path, format: str,
                       verbose: bool = True) -> None:
    """
    Saves the transcription results in the specified format.
    Args:
        results (Dict[str, Optional[str]]): Transcription results from Whisper.
        inputfile (Path): Original input file path (audio file).
        output_folder (Path): The folder where the transcription files should be stored.
        format (str): Desired format for the output file (e.g., 'tsv', 'txt', 'srt').
        verbose (bool): If True, print status updates. Default is True.
    Returns:
        None
    Raises:
        FileNotFoundError: If the output folder does not exist.
        Exception: For errors in file saving or writing.
    """
    try:
        # Ensure the output directory exists
        output_formatdir = Path(output_folder, 'raw', format)
        output_formatdir.mkdir(parents=True, exist_ok=True)

        # Create a writer for the specified format
        writer = get_writer(format, output_formatdir)

        # Replace the original file extension with the desired format extension
        output_filename = output_formatdir / f"{inputfile.stem}.{format}"

        # Save the transcription results
        writer(results, output_filename)
        if verbose:
            print(f"Saved {format} file to {output_filename}")
    except Exception as e:
        print(f"Error saving file {output_filename} in format {format}: {e}")