import requests
import isodate
from datetime import datetime, timedelta
import csv
import os
import yt_dlp
from config import YOUTUBE_API_KEY, WORKING_DIR, CHANNEL_IDS

def get_top_videos(channel_id, time_window_hours, max_duration_seconds, top_n_videos, language):
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(channel_url)
    channel_info = response.json()
    uploads_playlist_id = channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist_id}&maxResults=50&key={YOUTUBE_API_KEY}"
    response = requests.get(playlist_url)
    playlist_videos = response.json()

    video_ids = [video['snippet']['resourceId']['videoId'] for video in playlist_videos['items']]
    video_ids_string = ",".join(video_ids)

    details_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet,statistics&id={video_ids_string}&key={YOUTUBE_API_KEY}"
    details_response = requests.get(details_url)
    video_details = details_response.json()

    now = datetime.utcnow()
    time_window_ago = now - timedelta(hours=time_window_hours)

    recent_videos = []
    for video in video_details['items']:
        live_status = video['snippet'].get('liveBroadcastContent', 'none')
        if live_status != 'none':
            continue
        duration = video['contentDetails']['duration']
        publish_time = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        duration_seconds = isodate.parse_duration(duration).total_seconds()

        if publish_time > time_window_ago and duration_seconds < max_duration_seconds:
            recent_videos.append({
                'title': video['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={video['id']}",
                'view_count': int(video['statistics'].get('viewCount', 0)),
                'publish_time': publish_time,
                'duration': duration_seconds,
                'language': language
            })

    return sorted(recent_videos, key=lambda x: x['view_count'], reverse=True)[:top_n_videos]

def download_videos(videos, output_path):
    os.makedirs(output_path, exist_ok=True)
    csv_file_path = os.path.join(output_path, 'video_log.csv')

    # Initialize CSV with headers if it doesn’t exist
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'URL', 'Duration (s)', 'Filename', 'Language', 'Status', 'Transcription', 'Tweet'])

    class MyLogger:
        def debug(self, msg): pass
        def warning(self, msg): print(msg)
        def error(self, msg): print(msg)

    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'geo_bypass': True,
        'socket_timeout': 15,
        'ignoreerrors': True,
        'noplaylist': True,
        'live_from_start': False,
        'logger': MyLogger()
    }

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for video in videos:
                try:
                    info_dict = ydl.extract_info(video['url'], download=False)
                    if info_dict.get('is_live') or info_dict.get('was_live'):
                        print(f"Skipping live stream: {video['title']}")
                        continue
                    ydl.download([video['url']])
                    filename = ydl.prepare_filename(info_dict)
                    writer.writerow([video['title'], video['url'], video['duration'], filename, video['language'], 'downloaded', '', ''])
                    print(f"Downloaded: {video['title']}")
                except Exception as e:
                    print(f"Error downloading {video['title']}: {e}")
