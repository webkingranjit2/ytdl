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
    if not data:
        return jsonify({"success": False, "error": "No data received"})
        
    url = data.get('url')
    mode = data.get('mode')

    if not url:
        return jsonify({"success": False, "error": "URL missing"})

    # ইউটিউব ব্লক এড়াতে স্পেশাল কনফিগারেশন
    ydl_opts = {
        'format': 'best' if mode == 'mp4' else 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'add_header': [
            'Accept-Language: en-US,en;q=0.9',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ],
        # এটি ইউটিউবের নতুন সিকিউরিটি সিস্টেমের জন্য জরুরি
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর আসল ডেটা বের করা হচ্ছে
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ডাউনলোড লিঙ্ক খুঁজে বের করা
            video_url = info.get('url')
            
            if not video_url:
                # যদি সরাসরি url না থাকে, তবে formats থেকে সেরাটি খুঁজে নেবে
                formats = info.get('formats', [])
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        video_url = f.get('url')
                        break

            if video_url:
                return jsonify({"success": True, "download_url": video_url, "title": info.get('title', 'Video')})
            else:
                return jsonify({"success": False, "error": "Could not find a direct download link."})

    except Exception as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg:
            return jsonify({"success": False, "error": "YouTube is blocking our server. Please try a different link or wait."})
        return jsonify({"success": False, "error": error_msg})

if __name__ == "__main__":
    # Render এর জন্য পোর্ট অটোমেটিক সেট করা
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
