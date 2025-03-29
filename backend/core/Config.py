import os

# Define the base URL for media files
MEDIA_URL = os.getenv("MEDIA_URL", "/static/media/")

# Define the directory where media files will be stored
MEDIA_ROOT = os.path.join(os.getcwd(), "static", "media")

# Ensure the media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)
