"""
OpenAI Transcript Correction Script

====================================

Description:
This script automates the process of correcting raw transcripts using the OpenAI API.
It reads a raw transcript from a file, breaks it down into manageable chunks to meet token limits,
sends each chunk to OpenAI's language model (e.g., GPT-4), and retrieves the corrected version.
It supports both plain text files (.txt) and subtitle files (.srt), ensuring that any formatting
and timestamps in subtitle files are preserved. The corrected transcripts are saved in Markdown format (.md).

Main Features:
- Uses OpenAI's language model to correct transcripts in English or Dutch.
- Handles both .txt and .srt files, preserving structure and timestamps for subtitle files.
- Manages large transcripts by splitting them into chunks to fit within token limits for API requests.
- Retries API calls if rate limits are hit, with exponential backoff for retry attempts.
- Logs all activities, including errors, for transparency and debugging purposes.

Functions:
- `count_tokens(text: str) -> int`: Counts the number of tokens in a given text using the model's tokenizer.
- `chunk_text(text: str, max_tokens: int) -> list[str]`: Splits a transcript into chunks that fit within the token limit.
- `correct_transcript(raw_transcript: str, model: str) -> str`: Corrects a transcript using OpenAI’s language model.
- `correct_transcript_file(input_file: Path, output_file: Path, model: str) -> None`: Reads a transcript from a file, corrects it, and saves the result.

Requirements:
- Python 3.8 or higher.
- OpenAI Python library.
- A valid OpenAI API key, stored in a .env file.
- The `tiktoken` library for token counting.

Environment Variables:
- `.env` and `.env2` files should contain the OpenAI API key under the key 'OPENAI_API_KEY_KB_GENERAL'.

Usage:
1. Set up your OpenAI API key in a `.env` or `.env2` file.
2. Call the `correct_transcript_file` function with the paths to the input raw transcript and the output file,
   as well as the desired OpenAI model (e.g., 'gpt-4o').
3. The corrected transcript will be saved as a text (.txt) file.

Example:
    correct_transcript_file(
        input_file=Path("raw_transcript.txt"),
        output_file=Path("corrected_transcript.txt"),
        model="gpt-4o",
        delay_between_chunks=10
    )

Logging:
- Logs are generated for both normal operations and errors, including issues such as file not found, API rate limits, and saving errors.

Latest update: 22 October 2024
Author: Olaf Janssen (ookgezellig) - Strongly supported by ChatGPT
License: Creative Commons CC0 - http://creativecommons.org/publicdomain/zero/1.0
"""

from openai import OpenAI
from dotenv import dotenv_values
from pathlib import Path
import logging
import tiktoken  # Tokenization library for OpenAI models
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants for OpenAI API and model
TOKEN_LIMIT: int = 16000  # Maximum tokens allowed per request
TOKEN_BUFFER: int = 200  # Buffer to ensure we stay under the token limit

# Load OpenAI API key from environment variables
config = {**dotenv_values(".env"), **dotenv_values(".env2")}  # Merge two .env files
api_key_used = 'OPENAI_API_KEY_KB_GENERAL'
api_key = config.get(api_key_used)

if not api_key:
    logger.error(f"OpenAI API key '{api_key_used}' not found in the environment or .env files.")
    exit(1)

# Tokenizer setup for token counting
tokenizer = tiktoken.get_encoding("cl100k_base")  # Use appropriate tokenizer for the model

def count_tokens(text: str) -> int:
    """Counts the number of tokens in the given text using the model's tokenizer."""
    return len(tokenizer.encode(text))

def chunk_text(text: str, max_tokens: int) -> list[str]:
    """Splits a text into chunks that do not exceed the specified token limit."""
    # Call count_tokens to log the token count before chunking

    total_tokens = count_tokens(text)
    print('-'*50)
    print(f"Estimated tokens for this text: {total_tokens}")
    print('-'*50)

    tokens = tokenizer.encode(text)
    chunks = []
    current_chunk = []

    for token in tokens:
        if len(current_chunk) < max_tokens:
            current_chunk.append(token)
        else:
            chunks.append(tokenizer.decode(current_chunk))
            current_chunk = [token]

    # Append any remaining tokens as the last chunk
    if current_chunk:
        chunks.append(tokenizer.decode(current_chunk))

    return chunks

def correct_transcript(raw_transcript: str, model: str, delay_between_chunks: int = 10) -> str:
    """
    Corrects a raw transcript using OpenAI's language model.

    Args:
        raw_transcript (str): The full raw transcript to be corrected.
        model (str): The ChatGPT/OpenAI model (eg 'gpt-4o')
        delay_between_chunks (int): Number of seconds to wait between processing each chunk (default is 10 seconds).

    Returns:
        str: The corrected transcript as a single string.
    """
    max_tokens_per_chunk = TOKEN_LIMIT - TOKEN_BUFFER
    chunks = chunk_text(raw_transcript, max_tokens_per_chunk)

    corrected_chunks = []
    max_retries = 3  # Maximum retries per chunk
    initial_wait_time = 5  # Initial wait time for retries (seconds)
    backoff_factor = 2  # Exponential backoff factor

    for i, chunk in enumerate(chunks):
        logger.info(f"Correcting chunk {i + 1}/{len(chunks)}")
        try_count = 0

        while try_count < max_retries:
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system",
                         "content": "You are an assistant that helps with correcting transcripts in English or Dutch."},
                        {"role": "user", "content": f"""Here is a part of a raw, uncorrected
                        English audio transcript to be improved. This could be a .txt file or a .srt subtitle file.
                        If it is an .srt subtitle file, the formatting, structure, and all timestamps must be strictly preserved.
                        The original content must be fully preserved without any interpretation of paraphrasing words. 
                        So you should only improve the text of the transcript without translating any text from English to Dutch or vice versa. 
                        You are also not allowed to make any interpretations or add subheadings, etc. 
                        Here is the file: {chunk}"""}
                   ]
                )
                corrected_chunks.append(response.choices[0].message.content)
                break  # Exit retry loop on success

            except openai.RateLimitError as e:
                try_count += 1
                wait_time = initial_wait_time * (backoff_factor ** (try_count - 1))
                logger.warning(
                    f"Rate limit hit during OpenAI API call for chunk {i + 1}, attempt {try_count}. Waiting {wait_time} seconds before retrying.")
                time.sleep(wait_time)
                logger.error(f"Failed to correct chunk {i + 1} after {max_retries} attempts due to rate limit.")
                corrected_chunks.append(f"Error: Chunk {i + 1} could not be processed.")

            except openai.OpenAIError as e:
                try_count += 1
                logger.error(f"Error during OpenAI API call for chunk {i + 1}, attempt {try_count}: {e}")
                wait_time = initial_wait_time * (backoff_factor ** (try_count - 1))
                time.sleep(wait_time)

                if try_count >= max_retries:
                    logger.error(f"Failed to correct chunk {i + 1} after {max_retries} attempts.")
                    return None


        # Add a delay between processing chunks to ensure each chunk is fully processed
        logger.info(f"Waiting {delay_between_chunks} seconds before processing the next chunk...")
        time.sleep(delay_between_chunks)

    # Concatenate all corrected chunks
    corrected_transcript = "\n".join(corrected_chunks)
    logger.info('Full corrected transcript completed successfully.')
    return corrected_transcript

def correct_transcript_file(input_file: Path, output_file: Path, model: str, delay_between_chunks: int = 10) -> None:
    """
    Reads a raw transcript from a file, corrects it using OpenAI's language model, and saves the corrected version.

    Args:
        input_file (Path): Path to the raw transcript (.txt) file.
        output_file (Path): Path where the corrected transcript (.md) will be saved.
        model (str): The ChatGPT/OpenAI model (eg 'gpt-4o')
    """
    # Read the raw transcript file
    try:
        with input_file.open('r', encoding='utf-8') as file:
            raw_transcript = file.read()
    except FileNotFoundError as e:
        logger.error(f"File not found: {input_file}: {e}")
        return
    except Exception as e:
        logger.error(f"Error reading {input_file}: {e}")
        return

    # Correct the transcript using ChatGPT
    corrected_transcript = correct_transcript(raw_transcript, model, delay_between_chunks)
    if corrected_transcript is None:
        logger.error(f"Error correcting transcript for {input_file}")
        return

    # Save the corrected transcript as a text .txt file
    try:
        with output_file.open('w', encoding='utf-8') as file:
            file.write(corrected_transcript)
        logger.info(f"Corrected transcript saved: {output_file}")
    except Exception as e:
        logger.error(f"Error saving corrected transcript for {input_file}: {e}")