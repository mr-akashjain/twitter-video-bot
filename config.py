import os

# API Keys (loaded from environment variables)
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'YOUR_YOUTUBE_API_KEY_HERE')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'YOUR_GROQ_API_KEY_HERE')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', 'YOUR_TWITTER_API_KEY_HERE')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY', 'YOUR_TWITTER_API_SECRET_KEY_HERE')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', 'YOUR_TWITTER_ACCESS_TOKEN_HERE')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', 'YOUR_TWITTER_ACCESS_TOKEN_SECRET_HERE')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', 'YOUR_TWITTER_BEARER_TOKEN_HERE')

# Paths (configurable via environment variables)
WORKING_DIR = os.getenv('WORKING_DIR', './videos')
VOSK_MODEL_HINDI = os.getenv('VOSK_MODEL_HINDI', '/path/to/vosk-model-small-hi-0.22')
VOSK_MODEL_ENGLISH = os.getenv('VOSK_MODEL_ENGLISH', '/path/to/vosk-model-small-en-us-0.15')

# Language model paths dictionary
LANGUAGE_MODEL_PATHS = {
    'hindi': VOSK_MODEL_HINDI,
    'english': VOSK_MODEL_ENGLISH
}

# Default channel IDs
CHANNEL_IDS = {
    'ddnews': 'UCKwucPzHZ7zCUIf7If-Wo1g',  # DD News
    'reuters': 'UChqUTb7kYRX8-EiaN3XFrSQ'  # Reuters
}
