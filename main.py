import argparse
from download_videos import get_top_videos, download_videos
from transcribe_videos import transcribe_videos
from generate_comments import generate_comments
from post_tweets import post_tweets
from config import WORKING_DIR, CHANNEL_IDS

def main():
    parser = argparse.ArgumentParser(description="Twitter Video Bot")
    parser.add_argument('--download', action='store_true', help="Download videos")
    parser.add_argument('--transcribe', action='store_true', help="Transcribe videos")
    parser.add_argument('--generate', action='store_true', help="Generate comments")
    parser.add_argument('--post', action='store_true', help="Post tweets")
    args = parser.parse_args()

    csv_file = f"{WORKING_DIR}/video_log.csv"

    if args.download:
        videos = (
            get_top_videos(CHANNEL_IDS['ddnews'], 24, 600, 20, 'Hindi') +
            get_top_videos(CHANNEL_IDS['reuters'], 24, 600, 20, 'English')
        )
        download_videos(videos, WORKING_DIR)
    if args.transcribe:
        transcribe_videos(csv_file)
    if args.generate:
        generate_comments(csv_file)
    if args.post:
        post_tweets(csv_file)

if __name__ == "__main__":
    main()
