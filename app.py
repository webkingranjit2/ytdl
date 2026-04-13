import os
from flask import Flask, render_template, request, send_file
import yt_dlp
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format') # mp4 or mp3

    # ডাউনলোডের অপশনস
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
        'outtmpl': '-', # সরাসরি মেমোরিতে ডাউনলোড করবে
        'logtostderr': True,
    }

    if format_type == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
            # সরাসরি ভিডিওর লিঙ্কে রিডাইরেক্ট করা সবচেয়ে সহজ উপায়
            return f"<script>window.location.href='{video_url}';</script>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()
