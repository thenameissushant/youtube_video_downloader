from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from pytube import YouTube, Playlist
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']
    download_type = request.form['type']

    if download_type == 'video':
        try:
            yt = YouTube(url)
            if quality == 'highest':
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.get_lowest_resolution()
            stream.download(DOWNLOAD_FOLDER)
            return send_from_directory(DOWNLOAD_FOLDER, stream.default_filename, as_attachment=True)
        except Exception as e:
            return f"An error occurred: {str(e)}", 500
    elif download_type == 'playlist':
        try:
            playlist = Playlist(url)
            for video in playlist.videos:
                if quality == 'highest':
                    stream = video.streams.get_highest_resolution()
                else:
                    stream = video.streams.get_lowest_resolution()
                stream.download(DOWNLOAD_FOLDER)
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {str(e)}", 500
    else:
        return "Invalid download type", 400

if __name__ == '__main__':
    app.run(debug=True)
