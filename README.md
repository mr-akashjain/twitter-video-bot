# Twitter Video Bot

This project automates the process of downloading videos from YouTube, transcribing them using Vosk, generating comments with Groq, and posting tweets with videos (if under 140 seconds) or URLs (if over 140 seconds).

## Setup

### 1. Install Dependencies

#### Python Libraries:
```sh
pip install -r requirements.txt
```

#### FFmpeg:
Download and install [FFmpeg](https://ffmpeg.org/download.html). Ensure it is added to your system PATH.

#### Vosk Models:
Download the required Vosk models for Hindi and English. Update the paths in `config.py` accordingly.

### 2. Set Environment Variables

Set the following environment variables:

```plaintext
YOUTUBE_API_KEY
GROQ_API_KEY
TWITTER_API_KEY
TWITTER_API_SECRET_KEY
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
TWITTER_BEARER_TOKEN
WORKING_DIR (e.g., /path/to/videos)
VOSK_MODEL_HINDI
VOSK_MODEL_ENGLISH
```

#### On Unix/Linux/Mac:
```sh
export YOUTUBE_API_KEY='your_key_here'
```

#### On Windows:
```sh
set YOUTUBE_API_KEY=your_key_here
```

## Run the Script

### Full Workflow
Run all steps in the pipeline:
```sh
python main.py --download --transcribe --generate --post
```

### Specific Steps
To execute individual steps, use the corresponding flag. For example, to only download videos:
```sh
python main.py --download
```

## Usage

- Downloads the top 20 videos from DD News and Reuters (from the last 24 hours, under 10 minutes in duration).
- Transcribes the videos using Vosk (supports Hindi/English).
- Generates comments using Groq.
- Posts content to Twitter:
  - Videos are posted if they are less than 140 seconds.
  - URLs are posted if the video exceeds 140 seconds.

## Notes

- Ensure `FFmpeg` is available in your system PATH.
- Downloaded videos are stored in `WORKING_DIR`.
- `video_log.csv` tracks processing progress with a `Status` column.

