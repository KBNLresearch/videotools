# How to create high-quality offline video transcriptions and subtitles using Whisper and Python

<image src="media/afbeelding1.png" width="400" hspace="10" align="right"/>

I always thought that 'doing things with AI' was equivalant to smoking data centers, overheated servers, and massive cloud computing power.

My most jaw-dropping WTF OMG tech discovery of this month was discovering that those AI things can work just fine on your own modest laptop, and even offline! I was looking for a good solution to convert speech from a video file into text, also known as audio transcription, speech-to-text, or Automatic Speech Recognition (ASR).

## Why did I need audio transcriptions?
Using a video presentation I recently recorded, I wanted to do ASR, not only

* to **capture the full text** of my video, which will allow ChatGPT to create summaries, translations, blog posts or social media content from it, but also
* to automatically **create subtitles**, which I can add to the video to make it more accessible to deaf people, and thus meet the [WCAG](https://www.w3.org/TR/WCAG21/#abstract) guideline to [provide subtitles for video content](https://www.w3.org/WAI/media/av/captions/),
* and because it’s **fun and educational** to experiment with new tech, especially when it turns out to be easier than you initially estimated, giving useful and motivating 'let's-go-on' results quickly.

## Downsides of existing ASR services
Of course there are all kinds of existing audio-to-text cloud services, but they come with various downsides, including:

* Poor transcription quality, especially for names of things (so-called *named entities*, such as persons, places, organisations, journal titles etc.) and jargon words, which may need a lot of post-corrections;
* Limited number of supported languages;
* Privacy concerns: I want to avoid uploading my video to some sketchy AI transcription service, without knowing what will happen with it, especially when the source contains confidential content;
* Limited file sizes and/or video durations;
* Not wanting to publish your video on commercial platforms like YouTube, due to concerns about [public and open values](https://english.publicspaces.net/), despite it offering good transcription and subtitle features;
* Costs, paid subscriptions etc. 

For my little ASR project, I wanted to avoid these disadvantages as much as possible.

## *Whisper* as a solution
As I work with ChatGPT regularly, I had heard of [Whisper, OpenAI’s speech-to-text model](https://openai.com/index/whisper), but I never actually looked into it or used it. So I thought I’d give it a try!

After some research to see if this could suit my ASR (Automatic Speech Recognition) needs, I found out that [this model excels in Dutch](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages). But it also performs well in English.

<a href="https://nicobytes.com/blog/en/how-to-use-whisper/" target="_blank"><image src="media/afbeelding2.png" width="400" hspace="10" align="right"/></a>

OK, that already sounds promising. But Whisper doesn’t have a user-friendly front end (as far as I know), so I had to work with the API and Python. Fortunately, I found [this short blog post](https://nicobytes.com/blog/en/how-to-use-whisper/) to help me get started, and, combined with the [documentation](https://platform.openai.com/docs/guides/speech-to-text), it was straightforward to set up.

Further in this article, you’ll read about what I ultimately created with it and find ready-to-use Python code to try it out yourself.

## FFmpeg is needed
If you’re using the Whisper API with Python, you’ll need [FFmpeg](https://www.ffmpeg.org/) installed on your laptop. [Wikihow explains well](https://www.wikihow.com/Install-FFmpeg-on-Windows) how to set it up. Unfortunately, I couldn’t do this on my work laptop (no admin permissions!), so I did it at home on my personal laptop running Windows 10 Pro.

Here’s what it looks like on my home laptop. I followed the guide mentioned above.

<image src="media/ffmpeg-installatie-win10.PNG" width="100%" hspace="0" align="left"/>
<br clear="all" /><br>

<image src="media/ffmpeg-path-win10.PNG" width="100%" hspace="0" align="left"/>
<br clear="all" />

## Offline use, so privacy friendly
When you run this piece of Python code for the first time,

<image src="media/afbeelding4.png" width="400" hspace="10" align="right"/>

the ‘large’ model is downloaded to your machine once. (See here for [the available models](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).) To my great surprise, it’s just a 3GB file that handles all speech-to-text tasks without needing any further internet connection. So no smoking data centers, overheated servers, or massive cloud computing power—just a file on your own computer that you can use offline. And it’s great for privacy since everything happens offline on your own machine. Here’s the model on my home laptop. What happens inside that .pt file is pure magic!

<image src="media/whisper-models-location-win10.PNG" width="100%" hspace="0" align="left"/>
<br clear="all" />

## Speed
Does transcription go reasonably fast? The 'large-v2' model I use operates at about real-time speed, so if the audio is 15 minutes long, transcription takes about 15-20 minutes. The base and medium models are smaller and faster but deliver lower quality.

## And such quality! With subtitles! Even with poor input!
Beyond offline use, I am utterly amazed by the quality of the generated text. I’ll show this best through this (rather dull and quite lengthy) [test video](https://commons.wikimedia.org/wiki/File:Wikidata_Workshop_-_Theoretical_part_-_Maastricht_University_-_15_October_2024.webm) where I used myself as the test subject:

<image src="media/afbeelding5.png" width="100%" hspace="0" align="left"/>
<br clear="all" />

The unformatted block of text shown in the file description was fully created using Whisper, with only minimal post-correction. Pay particular attention to how well it generates all named entities and technical terms, including proper capitalization, etc. WOW!

As you can hear in the video, I’m certainly not making an effort to speak clearly, loudly, enthusiastically, fluently, or even lively. Even with such poor input (it was 1 a.m.), Whisper manages to produce a fantastic transcript purely from that 3GB .pt file (and FFmpeg)! Truly impressive!

And the [subtitles (closed captions)](https://commons.wikimedia.org/wiki/TimedText:Wikidata_Workshop_-_Theoretical_part_-_Maastricht_University_-_15_October_2024.webm.en.srt) you see in the video are also completely generated by Whisper, with the timing spot-on.

## Example code, try it yourself
To share my knowledge and code, I created the GitHub repo [https://github.com/KBNLresearch/videotools](https://github.com/KBNLresearch/videotools)

The relevant module is [transcribe_audio.py](../transcribe_audio.py), which is run from [runtools.py](../runtools.py), the main function of this repo.

If you want, you can have the audio transcript corrected by ChatGPT, for which I made an initial setup in [ai_correct_audiotranscripts.py](../ai_correct_audiotranscripts.py). To use this, you’ll need an [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key). But please note that you’ll lose the privacy advantage and offline use, as the ChatGPT models are far too large to run on a personal laptop.

As a side product, I also created a few other video and audio tools that only require FFmpeg, without a need for Whisper or ChatGPT.

<a href="https://github.com/KBNLresearch/videotools" target="_blank"><image src="media/afbeelding6.png" width="400" hspace="10" align="right"/></a>

## Questions, comments?
Since this was just a first experiment with this new piece of AI for me, I’d love to hear your questions, feedback, tips, etc. You can find my contact details below.

## Similar articles
*  [Super efficient! Subtitling or transcribing your video with AI](https://id.nl/huis-en-entertainment/computer-en-gaming/software/superefficient-je-video-ondertitelen-of-transcriberen-met-ai) (in Dutch)

## Licensing
<image src="media/icon_cc0.png" width="100" hspace="10" align="right"/>

All original materials in this repo, expect for the [blog article header](https://nicobytes.com/blog/en/how-to-use-whisper/) are released under the [CC0 1.0 Universal license](https://github.com/KBNLwikimedia/GLAMorousToHTML/blob/main/LICENSE), effectively donating all original content to the public domain.

## Contact
<image src="media/icon_kb2.png" width="200" hspace="10" align="right"/>

The [Videotools repo](https://github.com/KBNLresearch/videotools) is developed and maintained by Olaf Janssen, Wikimedia coordinator [@KB, national library of the Netherlands](https://www.kb.nl).
You can find his contact details on his [KB expert page](https://www.kb.nl/over-ons/experts/olaf-janssen) or via his [Wikimedia user page](https://commons.wikimedia.org/wiki/User:OlafJanssen).