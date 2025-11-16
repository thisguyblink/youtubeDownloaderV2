from flask import Flask, send_from_directory
import downloader

app = Flask(__name__)

@app.route("/")
def download(link, type, directory):
    downloader.flaskDownload(link, type, directory)