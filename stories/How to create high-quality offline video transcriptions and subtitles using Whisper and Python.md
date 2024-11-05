# How to create high-quality offline video transcriptions and subtitles using Whisper and Python

*Lastest update: 5 November 2024*

<image src="media/afbeelding1.png" width="400" hspace="10" align="right"/>

I used to think that 'doing things with AI' was equivalant to smoking data centers, overheated servers, and massive cloud computing power. But this month, I had a jaw-dropping WTF OMG tech discovery: realizing that some AI tasks can run smoothly on a modest laptop, and even offline! I was searching for a solid solution to convert speech from a video file into text (also known as audio transcription, speech-to-text, or Automatic Speech Recognition, ASR) and found that this can all happen right on my own machine.

## Why did I need audio transcriptions?
Using a recent video presentation I recorded, I wanted to apply ASR for several reasons:

- To **capture the full text** of my video, enabling ChatGPT to generate summaries, translations, blog posts, or social media content from it.
- To automatically **create subtitles**, enhancing accessibility for deaf and hard-of-hearing viewers and meeting the [WCAG](https://www.w3.org/TR/WCAG21/#abstract) guideline to [provide captions for video content](https://www.w3.org/WAI/media/av/captions/).
- And because it’s **fun and educational** to explore new technology, especially when it turns out easier than expected, delivering quick, motivating, and useful results that encourage further experimentation.

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

After some research to see if Whisper would suit my ASR needs, I found out that [this model excels in Dutch](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages), but it also performs very well in English.

<a href="https://nicobytes.com/blog/en/how-to-use-whisper/" target="_blank"><image src="media/afbeelding2.png" width="400" hspace="10" align="right"/></a>

So that sounded very promising. But (as far as I know) Whisper doesn’t offer a user-friendly front end, so I had to work with the API and Python. Fortunately, I found [this short blog post](https://nicobytes.com/blog/en/how-to-use-whisper/) to help me get started, and, combined with the [documentation](https://platform.openai.com/docs/guides/speech-to-text), it was quite straightforward to set things up.

Later in this article, you’ll see what I ultimately created with it, along with ready-to-use Python code so you can try it out for yourself.

## FFmpeg is needed
To use the Whisper API with Python, you’ll need to install [FFmpeg](https://www.ffmpeg.org/) on your laptop. [This WikiHow guide](https://www.wikihow.com/Install-FFmpeg-on-Windows) provides clear, step-by-step instructions for setup. I followed it on a laptop running Windows 10 Pro, and here’s what the setup looked like once completed.

<image src="media/ffmpeg-installatie-win10.PNG" width="100%" hspace="0" align="left"/>
<br clear="all" /><br>

<image src="media/ffmpeg-path-win10.PNG" width="100%" hspace="0" align="left"/>
<br clear="all" />

## Offline use, so privacy friendly
When you run this piece of Python code for the first time,

<image src="media/afbeelding4.png" width="400" hspace="10" align="right"/>

the ‘large’ model is downloaded to your machine once. (See here for [the available models](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).) To my great surprise, this turned out to be just a single 3GB file, handling all speech-to-text tasks, without needing any further internet connection. So no smoking data centers, overheated servers, or massive cloud computing power—just, but just a file on your own computer that you can use offline. Best of all, it’s great for privacy, as all processing happens entirely on your own device, ensuring your data stays private and secure.

Here’s a screenshot of the model on my home laptop. What happens inside that `.pt` file is pure magic!

<image src="media/whisper-models-location-win10.PNG" width="100%" hspace="0" align="left"/>
<br clear="all" />

## Speed
Does transcription run at a reasonable speed? With the 'large-v2' model I’m using, transcription operates at roughly real-time, so a 15-minute audio file takes about 15-20 minutes to process. Smaller models, like 'base' and 'medium,' are faster but typically produce lower-quality transcriptions.

## And such quality! With subtitles! Even with poor input!
Besides Whisper's offline capabilities, I am utterly amazed by the quality of the generated text. I can show this best through this (rather dull and quite lengthy) [test video](https://commons.wikimedia.org/wiki/File:Wikidata_Workshop_-_Theoretical_part_-_Maastricht_University_-_15_October_2024.webm) in which I used myself as the test subject:

<image src="media/afbeelding5.png" width="100%" hspace="0" align="left"/>
<br clear="all" />

The unformatted text block in the file description was generated entirely by Whisper, with only minimal human post-corrections. Take note of how accurately it handles named entities, technical terms, and proper capitalization, truly impressive!

In the video, you can tell I wasn’t making an effort to speak clearly, loudly, enthusiastically, or fluently. Yet, despite these less-than-ideal inputs, Whisper still managed to produce a fantastic transcription using just that 3GB `.pt` file (and FFmpeg). Absolutely amazing!

And the [subtitles (closed captions)](https://commons.wikimedia.org/wiki/TimedText:Wikidata_Workshop_-_Theoretical_part_-_Maastricht_University_-_15_October_2024.webm.en.srt) you see in the video were also completely generated by Whisper, in which all timings are spot-on as well.

## Example code, try it yourself
To share my knowledge and code, I created the GitHub repo [https://github.com/KBNLresearch/videotools](https://github.com/KBNLresearch/videotools)

The relevant module is [transcribe_audio.py](https://github.com/ookgezellig/videotools/blob/main/transcribe_audio.py), which is run from [runtools.py](https://github.com/ookgezellig/videotools/blob/main/runtools.py), the main function of this repo.

If you want, you can have the audio transcript corrected by ChatGPT, for which I made an initial setup in [ai_correct_audiotranscripts.py](https://github.com/ookgezellig/videotools/blob/main/ai_correct_audiotranscripts.py). To use this, you’ll need an [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key). But please note that you’ll lose the privacy advantage and offline use, as the ChatGPT models are far too large to run on a personal laptop.

As a side product, I also created a few other video and audio tools that only require FFmpeg, without a need for Whisper or ChatGPT.

<a href="https://github.com/KBNLresearch/videotools" target="_blank"><image src="media/afbeelding6.png" width="400" hspace="10" align="right"/></a>

## Questions, comments?
Since this was just a first experiment with this new piece of AI for me, I’d love to hear your questions, feedback, tips, etc. You can find my contact details below.

## Similar articles
*  [Super efficient! Subtitling or transcribing your video with AI](https://id.nl/huis-en-entertainment/computer-en-gaming/software/superefficient-je-video-ondertitelen-of-transcriberen-met-ai) (in Dutch)

## Licensing
<image src="media/icon_cc0.png" width="100" hspace="10" align="right"/>

All original materials in this repo, expect for the [blog article header](https://nicobytes.com/blog/en/how-to-use-whisper/), are released under the [CC0 1.0 Universal license](https://github.com/KBNLwikimedia/GLAMorousToHTML/blob/main/LICENSE), effectively donating all original content to the public domain.

## Contact
<image src="media/icon_kb2.png" width="200" hspace="10" align="right"/>

The [Videotools repo](https://github.com/KBNLresearch/videotools) is developed and maintained by Olaf Janssen, Wikimedia coordinator [@KB, national library of the Netherlands](https://www.kb.nl).
You can find his contact details on his [KB expert page](https://www.kb.nl/over-ons/experts/olaf-janssen) or via his [Wikimedia user page](https://commons.wikimedia.org/wiki/User:OlafJanssen).