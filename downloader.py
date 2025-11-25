from pytubefix import YouTube, Search
from pytubefix.cli import on_progress
import subprocess
import re
import argparse
import requests
import base64
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')

# https://open.spotify.com/playlist/34VAWXMq6tGpcIcg15AXxL?si=71028e9d1a964a08

def main():
    link, type = getArgs()
    youtubeLinks = []
    token = getSpotifyToken()
    if checkSpotifyLink(link):
        name, songList = getSongsFromSpotify(token, link)
        for title, artists in songList:
            query = f"{title} {' '.join(artists)}"
            youtubeLinks.append(safe_search(query))
    else:
        youtubeLinks.append(link)
    if len(youtubeLinks) > 1:
        folderName = "".join(word.capitalize() for word in name.split())
        os.mkdir(folderName)
        os.chdir(folderName)
    for link in youtubeLinks:
        download(link, type)
    subprocess.run(["../cleanup.sh", folderName, type])

    
def download(url, format) -> str:
    yt = YouTube(url, on_progress_callback=on_progress)
    songName = yt.title
    safeName = re.sub(r'[\\/*?:"<>|]', "", songName)
    if format == "mp4":
        ys = yt.streams.get_highest_resolution()
    else:
        ys = yt.streams.get_audio_only()
    downloadedFile = ys.download()
    outputFile = safeName + "." + format
    subprocess.run(["ffmpeg", "-i", downloadedFile, outputFile], check=True)
    return outputFile


def safe_search(query, retries=3, delay=2):
    for attempt in range(retries):
        try:
            results = Search(query)
            if not results.videos:
                return None
            return results.videos[0].watch_url
        except Exception as e:
            print(f"Search failed ({e}). Retrying {attempt+1}/{retries}...")
            time.sleep(delay)
    raise Exception(f"Search failed after {retries} retries: {query}")

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", help="Link for Spotify Playlist or youtube Video")
    parser.add_argument("-t", "--type", help="Type of download, mp4, mp3 or wav")
    args = parser.parse_args()
    return args.link, args.type

def checkSpotifyLink(link):
    return "spotify.com" in link


def getSpotifyToken():
    encoded = base64.b64encode((clientID + ":" + clientSecret).encode("ascii")).decode("ascii")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + encoded
    }

    payload = {
        "grant_type": "client_credentials"
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers,
                             auth=(clientID, clientSecret))
    json_response = json.loads(response.content)
    global token
    token = json_response["access_token"]
    return token


def getAuthHeader(token):
    return {"Authorization": "Bearer " + token}


def getSongsFromSpotify(token, link):
    playlist_url = "https://api.spotify.com/v1/playlists/"
    headers = getAuthHeader(token)
    playlist_id = link.split("playlist/")[1]
    head, sep, tail = playlist_id.partition("?")
    playlist_id = head
    query_url = playlist_url + playlist_id
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)
    name = json_result['name']
    tracks = json_result["tracks"]['items']

    songs = []
    for track in tracks:
        song = track['track']
        songTitle = song['name']
        artists = [artist['name'] for artist in song['artists']]
        songs.append((songTitle, artists))
    
    return name, songs

if __name__ == "__main__":
    main()

#  python3 downloader.py -l "https://open.spotify.com/playlist/34VAWXMq6tGpcIcg15AXxL?si=71028e9d1a964a08" -t mp3
