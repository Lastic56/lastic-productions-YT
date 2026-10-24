FROM python:3.11-slim

# Install FFmpeg for audio conversion (MP3/M4A/WAV)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY Flask\ app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY Flask\ app/ .

# Expose port Render uses
ENV PORT=10000

# Start gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
