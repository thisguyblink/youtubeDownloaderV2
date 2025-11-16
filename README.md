# Youtube Downloader V2

## Instructions
1. Clone repo onto local machine
2. Make a new virtual environment
3. Activate virtual environment 
4. Install requirements from requirements.txt
5. Run comand to download youtube video or Spotify Playlist(Example Input Below)

## Disclaimer 
In order to download a playlist from spotify you must make a developer account\
Then you must make a new project\
Then make a .env file and put you Client Id and Client Secret in the file

### Env Example
```dotenv
CLIENT_ID=238odhu23hedi328238hedu2u3923
CLIENT_SECRET=2139ued9923e8hd92398982398d
```

## Making New Virtual Enviornment 
```commandline
/opt/homebrew/bin/python3 -m venv .venv
```

## Activating Virtual Enviornment 
```commandline
source .venv/bin/activate
```

## Installing requirements through cli
```commandline
pip3 install -r requirements.txt
```

## Command Line Usage Template 
```commandline
python3 downloader.py -l (link) -t (mp4 or mp3 or wav)
```

## Downloading Youtube Video as mp3
```commandline
python3 downloader.py -l https://www.youtube.com/watch?v=Aq5WXmQQooo&list=RDAq5WXmQQooo&start_radio=1&pp=ygUJcmljayByb2xsoAcB -t mp3
```

## Downloading Youtube Video as mp4
```commandline
python3 downloader.py -l https://www.youtube.com/watch?v=Aq5WXmQQooo&list=RDAq5WXmQQooo&start_radio=1&pp=ygUJcmljayByb2xsoAcB -t mp4
```

## Downloading Spotify Playlists as wav
```commandline
python3 downloader.py -l https://open.spotify.com/playlist/69GPWNeR9uA3N0i1iYfGgx?si=d5eaf763aed6479e -t wav
```






