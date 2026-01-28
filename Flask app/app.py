from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import threading
import yt_dlp
import datetime
import webbrowser
from threading import Timer

app = Flask(__name__)

# Global storage for download progress
download_status = {
    'status': 'Ready',
    'progress': 0,
    'speed': 'N/A',
    'eta': 'N/A',
    'title': '',
    'error': None,
    'finished': False
}

class YtdlpLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): 
        print(f"YTDLP ERROR: {msg}")
        download_status['error'] = msg

def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            p = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            download_status['progress'] = round(p, 1)
            download_status['speed'] = d.get('_speed_str', 'N/A')
            download_status['eta'] = d.get('_eta_str', 'N/A')
            download_status['status'] = f"Downloading: {download_status['progress']}%"
        except:
            pass
    elif d['status'] == 'finished':
        download_status['status'] = "Processing..."
        download_status['progress'] = 100

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            valid_qualities = set()
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none':
                    height = f.get('height')
                    if height: valid_qualities.add(f"{height}p")
            
            sorted_qualities = sorted(list(valid_qualities), key=lambda x: int(x.replace('p', '')), reverse=True)
            sorted_qualities.insert(0, 'Best')
            sorted_qualities.append('Audio Only')
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'qualities': sorted_qualities
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    quality = data.get('quality')
    audio_format = data.get('audio_format', 'mp3')
    bitrate = data.get('bitrate', '320')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Reset status
    download_status.update({
        'status': 'Initializing...',
        'progress': 0,
        'finished': False,
        'error': None
    })

    thread = threading.Thread(target=run_download, args=(url, quality, audio_format, bitrate))
    thread.start()
    return jsonify({'message': 'Download started'})

def run_download(url, quality, audio_format, bitrate):
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    ydl_opts = {
        'progress_hooks': [progress_hook],
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'logger': YtdlpLogger()
    }

    if quality == 'Audio Only':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': bitrate
        }]
    elif quality == 'Best':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    else:
        height = quality.replace('p', '')
        ydl_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            download_status['title'] = info.get('title', 'Video')
            download_status['status'] = "Completed"
            download_status['finished'] = True
    except Exception as e:
        download_status['error'] = str(e)
        download_status['status'] = "Error"

@app.route('/status')
def status():
    return jsonify(download_status)

if __name__ == '__main__':
    # Get local IP
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    
    print(f"\n* Lastic Productions Flask Server Ready!")
    print(f"* Local Address: http://127.0.0.1:5000")
    print(f"* Network Address: http://{ip}:5000 (Open this on your phone!)\n")
    
    # Auto-open browser on launch
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000")
    
    Timer(1.5, open_browser).start()
    
    app.run(host='0.0.0.0', port=5000, debug=False) # Turned off debug for cleaner launch
