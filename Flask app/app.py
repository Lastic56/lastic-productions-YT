from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
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

    ydl_opts = {
        'quiet': True, 
        'no_warnings': True,
        'logger': YtdlpLogger(),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'player_skip': ['configs', 'webpage'],
            }
        },
        'socket_timeout': 30,
        'retries': 3
    }
    try:
        print(f"Analyzing URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"Successfully extracted info for: {info.get('title', 'Unknown')}")
            
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
        print(f"Error analyzing URL: {str(e)}")
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
    # Unified local project storage for cloud hosting compatibility
    local_download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(local_download_dir):
        os.makedirs(local_download_dir)

    ydl_opts = {
        'progress_hooks': [progress_hook],
        'outtmpl': os.path.join(local_download_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'logger': YtdlpLogger(),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'video',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web'],
                'player_skip': ['configs', 'webpage', 'js'],
                'po_token': ['android', 'ios'],
            }
        },
        'extractor_retries': 5,
        'fragment_retries': 10,
        'retry_sleep_functions': {
            'http': lambda x: min(x * 2, 60),
            'fragment': lambda x: min(x * 2, 60),
            'file_access': lambda x: min(x * 2, 30)
        },
        'file_access_retries': 10,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'extract_flat': False,
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
            download_status['file_path'] = ydl.prepare_filename(info)
            download_status['status'] = "Completed"
            download_status['finished'] = True
    except Exception as e:
        download_status['error'] = str(e)
        download_status['status'] = "Error"

@app.route('/status')
def status():
    return jsonify(download_status)

@app.route('/get_file')
def get_file():
    path = download_status.get('file_path')
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Media file not found. Please try downloading again.", 404

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
