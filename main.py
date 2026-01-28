import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.animation import Animation

import threading
import os
import yt_dlp
import sys
import datetime

# Helper to check permissions on Android
class YtdlpLogger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(f"YTDLP ERROR: {msg}")

def check_permissions():
    if platform == "android":
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])

KV = '''
<MainLayout>:
    orientation: 'vertical'
    spacing: '10dp'
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.05, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # --- Modern App Bar ---
    BoxLayout:
        size_hint_y: None
        height: '60dp'
        padding: ['15dp', '5dp']
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: 'LASTIC PRODUCTIONS'
            font_size: '20sp'
            bold: True
            halign: 'left'
            valign: 'middle'
            text_size: self.size
            color: 0, 0.7, 1, 1

    BoxLayout:
        orientation: 'vertical'
        padding: '15dp'
        spacing: '15dp'

        # --- Input Section ---
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: '90dp'
            spacing: '8dp'

            Label:
                text: 'ENTER VIDEO URL'
                font_size: '12sp'
                bold: True
                color: 0.6, 0.6, 0.6, 1
                size_hint_y: None
                height: '20dp'
                halign: 'left'
                text_size: self.size

            BoxLayout:
                size_hint_y: None
                height: '50dp'
                spacing: '10dp'

                TextInput:
                    id: url_input
                    hint_text: 'Paste YouTube/Social link...'
                    multiline: False
                    background_normal: ''
                    background_color: 0.15, 0.15, 0.15, 1
                    foreground_color: 1, 1, 1, 1
                    cursor_color: 0, 0.7, 1, 1
                    padding: ['12dp', '13dp']
                    font_size: '16sp'
                    on_text_validate: root.fetch_info_threaded()

                Button:
                    text: 'GET'
                    size_hint_x: None
                    width: '70dp'
                    background_normal: ''
                    background_color: 0, 0.5, 0.8, 1
                    bold: True
                    on_release: root.fetch_info_threaded()

        # --- Preview Card ---
        BoxLayout:
            id: info_card
            orientation: 'vertical'
            size_hint_y: None
            height: '140dp' if root.video_title else 0
            opacity: 1 if root.video_title else 0
            padding: '10dp'
            spacing: '10dp'
            canvas.before:
                Color:
                    rgba: 0.12, 0.12, 0.12, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10,]

            BoxLayout:
                spacing: '12dp'
                AsyncImage:
                    id: thumbnail
                    source: ''
                    size_hint_x: 0.4
                    allow_stretch: True
                    keep_ratio: True
                
                Label:
                    id: video_title_label
                    text: root.video_title
                    font_size: '14sp'
                    text_size: self.width, None
                    size_hint_x: 0.6
                    valign: 'middle'
                    halign: 'left'
                    max_lines: 4
                    shorten: True

        # --- Quality Selection ---
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: '10dp'
            
            BoxLayout:
                size_hint_y: None
                height: '45dp'
                spacing: '10dp'
                Label:
                    text: 'Format:'
                    size_hint_x: 0.3
                    halign: 'left'
                    text_size: self.size
                Spinner:
                    id: quality_spinner
                    text: 'Select Quality'
                    values: []
                    background_normal: ''
                    background_color: 0.2, 0.2, 0.2, 1

            # Audio Specific Controls
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: '100dp' if 'Audio' in quality_spinner.text else 0
                opacity: 1 if 'Audio' in quality_spinner.text else 0
                spacing: '8dp'
                
                BoxLayout:
                    size_hint_y: None
                    height: '45dp'
                    spacing: '10dp'
                    Label:
                        text: 'Codec:'
                        size_hint_x: 0.3
                        halign: 'left'
                        text_size: self.size
                    Spinner:
                        id: audio_format_spinner
                        text: 'MP3'
                        values: ('MP3', 'M4A', 'WAV')
                        background_normal: ''
                        background_color: 0.3, 0.1, 0.4, 1

                BoxLayout:
                    size_hint_y: None
                    height: '45dp'
                    spacing: '10dp'
                    Label:
                        text: 'Bitrate:'
                        size_hint_x: 0.3
                        halign: 'left'
                        text_size: self.size
                    Spinner:
                        id: audio_quality_spinner
                        text: '320'
                        values: ('320', '256', '192', '128', '64')
                        background_normal: ''
                        background_color: 0.3, 0.1, 0.4, 1

        # --- Action Buttons ---
        BoxLayout:
            size_hint_y: None
            height: '55dp'
            spacing: '12dp'

            Button:
                id: download_btn
                text: 'DOWNLOAD VIDEO'
                background_normal: ''
                background_color: 0, 0.7, 0, 1
                bold: True
                disabled: True
                border_radius: [20,]
                on_release: root.start_download()

            Button:
                id: mp3_btn
                text: 'QUICK MP3'
                size_hint_x: 0.4
                background_normal: ''
                background_color: 0.5, 0, 0.8, 1
                bold: True
                disabled: True
                on_release: root.start_mp3_download()

        # --- Progress ---
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: '60dp'
            spacing: '2dp'
            
            Label:
                id: status_label
                text: 'READY'
                font_size: '14sp'
                bold: True
                color: 0.8, 0.8, 0.8, 1

            ProgressBar:
                id: progress_bar
                max: 100
                value: 0
                size_hint_y: None
                height: '10dp'

            Label:
                id: speed_eta_label
                text: ''
                font_size: '11sp'
                color: 0.5, 0.5, 0.5, 1

        # --- Log ---
        ScrollView:
            id: log_scroll
            scroll_type: ['bars', 'content']
            bar_width: '4dp'
            canvas.before:
                Color:
                    rgba: 0.08, 0.08, 0.08, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [5,]

            Label:
                id: log_label
                text: '[i]Log initialized...[/i]\\n'
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                padding: '10dp', '10dp'
                markup: True
                font_size: '11sp'
                color: 0.7, 0.7, 0.7, 1

        Button:
            text: 'CLEAR LOG'
            size_hint_y: None
            height: '40dp'
            background_normal: ''
            background_color: 0.3, 0.3, 0.3, 1
            font_size: '12sp'
            on_release: root.clear_log()
'''

class MainLayout(BoxLayout):
    video_title = ObjectProperty('')
    
    def log(self, message):
        print(f"MOBILE_LOG: {message}")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.ids.log_label.text += f"[color=666666][{timestamp}][/color] {message}\\n"
        Clock.schedule_once(self._scroll_to_bottom)

    def _scroll_to_bottom(self, dt):
        self.ids.log_scroll.scroll_y = 0
        
    def clear_log(self):
        self.ids.log_label.text = '[i]Log cleared...[/i]\\n'
        self.ids.progress_bar.value = 0
        self.ids.status_label.text = 'READY'
        self.ids.speed_eta_label.text = ''

    def fetch_info_threaded(self):
        url = self.ids.url_input.text.strip()
        if not url:
            self.log("No URL provided.")
            return
        
        self.ids.status_label.text = "ANALYZING..."
        self.ids.quality_spinner.text = "Fetching info..."
        self.ids.download_btn.disabled = True
        self.ids.mp3_btn.disabled = True
        
        threading.Thread(target=self.fetch_info, args=(url,), daemon=True).start()

    def fetch_info(self, url):
        ydl_opts = {'quiet': True, 'no_warnings': True, 'logger': YtdlpLogger()}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                thumb = info.get('thumbnail', '')
                
                valid_qualities = set()
                for f in info.get('formats', []):
                    if f.get('vcodec') != 'none':
                        height = f.get('height')
                        if height: valid_qualities.add(f"{height}p")
                
                sorted_qualities = sorted(list(valid_qualities), key=lambda x: int(x.replace('p', '')), reverse=True)
                sorted_qualities.insert(0, 'Best')
                sorted_qualities.append('Audio Only')
                
                Clock.schedule_once(lambda dt: self.update_ui_with_info(title, thumb, sorted_qualities))
        except Exception as e:
            err = str(e)
            Clock.schedule_once(lambda dt: self.error_ui(f"Error: {err[:40]}"))

    def update_ui_with_info(self, title, thumb, qualities):
        self.video_title = title
        self.ids.thumbnail.source = thumb
        self.ids.quality_spinner.values = qualities
        self.ids.quality_spinner.text = 'Best'
        self.ids.download_btn.disabled = False
        self.ids.mp3_btn.disabled = False
        self.ids.status_label.text = "READY TO DOWNLOAD"
        self.log(f"Analyzed: {title[:30]}...")

    def start_mp3_download(self):
        self.ids.quality_spinner.text = "Audio Only"
        self.ids.audio_format_spinner.text = "MP3"
        self.ids.audio_quality_spinner.text = "320"
        self.start_download()

    def start_download(self):
        url = self.ids.url_input.text.strip()
        quality_text = self.ids.quality_spinner.text
        audio_format = self.ids.audio_format_spinner.text.lower() if 'Audio' in quality_text else None
        audio_quality = self.ids.audio_quality_spinner.text if 'Audio' in quality_text else None
        
        if not url: return

        # Default path selection
        if platform == "android":
            from android.storage import primary_external_storage_path
            download_dir = os.path.join(primary_external_storage_path(), 'Download')
        else:
            download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            
        if not os.path.exists(download_dir): os.makedirs(download_dir)

        self.ids.status_label.text = "INITIALIZING..."
        self.ids.download_btn.disabled = True
        self.ids.mp3_btn.disabled = True
        
        threading.Thread(target=self.download_thread, args=(url, quality_text, download_dir, audio_format, audio_quality), daemon=True).start()

    def download_thread(self, url, quality_text, download_dir, audio_format, audio_quality):
        ydl_opts = {
            'progress_hooks': [self.progress_hook],
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'quiet': True, 'no_warnings': True, 'logger': YtdlpLogger()
        }

        if quality_text == 'Audio Only':
            ydl_opts['format'] = 'bestaudio/best'
            codec = audio_format or 'mp3'
            bitrate = audio_quality or '320'
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': codec, 'preferredquality': bitrate}]
        elif quality_text == 'Best':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        else:
            height = quality_text.replace('p', '')
            ydl_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                Clock.schedule_once(lambda dt: self.success_ui(info.get('title', 'Video')))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.error_ui(str(e)))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                progress = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                Clock.schedule_once(lambda dt: self.update_progress(progress, speed, eta))
            except: pass
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.update_status("PROCESSING..."))

    def update_progress(self, progress, speed, eta):
        self.ids.progress_bar.value = progress
        self.ids.status_label.text = f"DOWNLOADING: {progress:.1f}%"
        self.ids.speed_eta_label.text = f"{speed} | ETA: {eta}"

    def update_status(self, msg):
        self.ids.status_label.text = msg

    def success_ui(self, title):
        self.ids.progress_bar.value = 100
        self.ids.status_label.text = "✔️ DOWNLOAD COMPLETE"
        self.ids.speed_eta_label.text = ""
        self.ids.download_btn.disabled = False
        self.ids.mp3_btn.disabled = False
        self.log(f"Success: {title[:20]}...")
        
        anim = Animation(color=(0, 1, 0.2, 1), font_size='16sp', duration=0.2)
        anim += Animation(color=(0.8, 0.8, 0.8, 1), font_size='14sp', duration=0.4)
        anim.start(self.ids.status_label)

    def error_ui(self, msg):
        self.ids.status_label.text = "❌ ERROR"
        self.log(f"Error: {msg[:50]}")
        self.ids.download_btn.disabled = False
        self.ids.mp3_btn.disabled = False

class MobileDownloaderApp(App):
    title = "Lastic Productions Mobile"
    def build(self):
        Builder.load_string(KV)
        return MainLayout()

if __name__ == '__main__':
    MobileDownloaderApp().run()
