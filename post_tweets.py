import os
import subprocess
import time
import csv
from pytwitter import Api
from config import TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, WORKING_DIR

api = Api(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET_KEY,
    access_token=TWITTER_ACCESS_TOKEN,
    access_secret=TWITTER_ACCESS_TOKEN_SECRET
)

def get_video_duration(input_video):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None

def convert_video(input_video):
    output_video = input_video.rsplit('.', 1)[0] + '_temp.mp4'
    try:
        subprocess.run(['ffmpeg', '-i', input_video, '-vcodec', 'libx264', '-acodec', 'aac', '-b:v', '5M', '-vf', 'scale=1280:720', '-preset', 'fast', '-y', output_video], check=True)
        os.replace(output_video, input_video)
        print(f"Converted: {input_video}")
    except Exception as e:
        print(f"Error converting {input_video}: {e}")

def upload_video_chunked(video_path):
    total_bytes = os.path.getsize(video_path)
    init_response = api.upload_media_chunked_init(total_bytes=total_bytes, media_type="video/mp4")
    media_id = init_response.media_id_string

    segment_size = 5 * 1024 * 1024
    with open(video_path, "rb") as video_file:
        segment_index = 0
        while True:
            chunk = video_file.read(segment_size)
            if not chunk:
                break
            api.upload_media_chunked_append(media_id=media_id, media=chunk, segment_index=segment_index)
            segment_index += 1

    finalize_response = api.upload_media_chunked_finalize(media_id=media_id)
    while finalize_response.processing_info and finalize_response.processing_info.state not in ['succeeded', 'failed']:
        time.sleep(50)
        finalize_response = api.upload_media_chunked_status(media_id=media_id)
    if finalize_response.processing_info.state == 'failed':
        raise Exception("Video processing failed.")
    return media_id

def post_tweets(csv_file):
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        if row['Status'] != 'comment_generated':
            continue
        video_path = os.path.join(WORKING_DIR, row['Filename'])
        duration = float(row['Duration (s)'])
        
        if duration > 140:
            api.create_tweet(text=row['Tweet'])
            row['Status'] = 'tweeted'
            print(f"Tweeted URL for: {row['Title']}")
        else:
            if os.path.exists(video_path):
                convert_video(video_path)
                media_id = upload_video_chunked(video_path)
                api.create_tweet(text=row['Tweet'], media_media_ids=[media_id])
                row['Status'] = 'tweeted'
                print(f"Tweeted video for: {row['Title']}")
                time.sleep(880)

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
