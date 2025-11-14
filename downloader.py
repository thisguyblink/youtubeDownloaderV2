from pytubefix import YouTube, Search
from pytubefix.cli import on_progress
import subprocess
import re
import sys

def main(): 
    action = sys.argv[1]
    if action == "help":
        print("file (down:search) (link:`search query`) (mp3:wav)")
    param = sys.argv[2]
    downloadType = sys.argv[3]
    if action == None:
        print("No action given, exiting now")
        return
    if (param == None):
        print("No Link given")
        return
    elif downloadType == None: 
        print("No download type given")
        return 
    if action == "down":
        downloadAudio(param, downloadType)
    elif action == "search":
        link = search(param)
        downloadAudio(link, downloadType)
    else:
        print("Chose download with the `down` argument and search with the `search` argument")
    
def downloadAudio(url, format) -> str:
    yt = YouTube(url, on_progress_callback=on_progress)
    songName = yt.title
    safeName = re.sub(r'[\\/*?:"<>|]', "", songName)
    ys = yt.streams.get_audio_only()   
    downloadedFile = ys.download()
    print(f"Song Name: {safeName}")
    if (format == "mp3"):
        outputFile = safeName + ".mp3"
    elif (format == "wav"):
        outputFile = safeName + ".wav"
    subprocess.run(["ffmpeg", "-i", downloadedFile, outputFile], check=True)
    return outputFile

def search(query):
    results = Search('GitHub Issue Best Practices')
    video = results.videos[0]
    print(f"This is the title of the first video found{video.title}")
    return video.watch_url

