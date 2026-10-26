FROM python:3.11-slim

# Install FFmpeg for audio conversion (MP3/M4A/WAV)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY ["Flask app/requirements.txt", "./"]
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what the app needs (exclude build/, dist/, __pycache__)
COPY ["Flask app/app.py", "./"]
COPY ["Flask app/wsgi.py", "./"]
COPY ["Flask app/templates/", "./templates/"]
COPY ["Flask app/static/", "./static/"]

# Render provides $PORT; default to 10000
ENV PORT=10000

# gunicorn with threads so background download requests don't block the UI polling
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 app:app
