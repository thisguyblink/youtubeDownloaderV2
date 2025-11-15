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

load_dotenv()
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')

# https://open.spotify.com/playlist/34VAWXMq6tGpcIcg15AXxL?si=71028e9d1a964a08

def main():
    link, type = getArgs()
    youtubeLinks = []
    token = getSpotifyToken()
    if checkSpotifyLink(link):
        songList = getSongsFromSpotify(token, link)
        for song in songList:
            youtubeLinks.append(search(song))
    else:
        youtubeLinks.append(link)
    if len(youtubeLinks) > 1:
        os.mkdir("downloadedFiles")
        os.chdir("downloadedFiles")
    for link in youtubeLinks:
        download(link, type)
    os.chdir("..")
    
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
    print(f"Output File name: {outputFile}")
    subprocess.run(["ffmpeg", "-i", downloadedFile, outputFile], check=True)
    return outputFile


def search(query):
    results = Search(query)
    video = results.videos[0]
    print(f"This is the title of the first video found{video.title}")
    return video.watch_url

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", help="Link for Spotify Playlist or youtube Video")
    parser.add_argument("-t", "--type", help="Type of download, mp4, mp3 or wav")
    args = parser.parse_args()
    print(args.link)
    print(args.type)
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
    songQueries = []
    playlist_id = link.split("playlist/")[1]
    head, sep, tail = playlist_id.partition("?")
    playlist_id = head
    query_url = playlist_url + playlist_id + "/tracks"
    offset = 0
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)
    total_songs = 0
    num_tracks = json_result['total']
    loop = int(num_tracks / 50)
    if num_tracks % 50 > 1:
        loop += 1
    for i in range(loop):  # loop through requests 50 at a time while adding to offset
        query_url + "?limit=50&offset={}"
        query_url.format(offset)
        result = requests.get(query_url, headers=headers)
        json_result = json.loads(result.content)
        for j in range(50):
            if num_tracks > 0:
                trackId = (json_result['items'][j]['track']['id'])
                songQueries.append(trackSearch(trackId))
                num_tracks -= 1
                total_songs += 1
            else:
                break
        head, sep, tail = query_url.partition("?")
        query_url = head
        offset += 50
    return songQueries


def trackSearch(id):
    url = "https://api.spotify.com/v1/tracks/"
    query_url = url + id
    print(query_url)
    header = getAuthHeader(token)
    result = requests.get(query_url, headers=header)
    json_result = json.loads(result.content)
    name = json_result['name']
    artist = json_result['artists'][0]['name']
    search = name + " by " + artist
    return search

if __name__ == "__main__":
    main()

# python3 downloader.py https://open.spotify.com/playlist/34VAWXMq6tGpcIcg15AXxL?si=71028e9d1a964a08 mp3

