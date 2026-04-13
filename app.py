import os
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    mode = data.get('mode')

    if not url:
        return jsonify({"success": False, "error": "URL missing"})

    ydl_opts = {
        'format': 'best' if mode == 'mp4' else 'bestaudio',
        'quiet': True,
        'no_warnings': True,
        # কুকি ফাইল ব্যবহার করা হচ্ছে
        'cookiefile': 'cookies.txt',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            return jsonify({"success": True, "download_url": video_url})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run()
