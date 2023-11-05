import os
import json
import datetime
import pickle
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import hashlib

load_dotenv()

# API Key
API_KEY = os.environ.get("YOUTUBE_DATA_API_KEY")

# Permissions
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    return build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

# Function to compute the checksum for a video ID
def compute_checksum(video_id):
    return hashlib.sha256(video_id.encode()).hexdigest()

# Function to check if the video is new based on checksum
def is_video_new(video_id, checksum_record):
    checksum = compute_checksum(video_id)
    return checksum not in checksum_record


def get_video_data(youtube, playlist_id):
    page_token = None
    all_video_data = []
    cache_file = 'data/cache/cache.pkl'

    try:
        with open(cache_file, 'rb') as f:
            all_video_data = pickle.load(f)
    except FileNotFoundError:
        pass

    while True:
        try:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,  # max allowed value
                pageToken=page_token
            )
            response = request.execute()
            video_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
            videos_request = youtube.videos().list(
                part="id,statistics,contentDetails,snippet",
                id=','.join(video_ids)
            )
            videos_response = videos_request.execute()
            all_video_data.extend(videos_response['items'])

            with open(cache_file, 'wb') as f:
                pickle.dump(all_video_data, f)

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        except HttpError as e:
            print(f"HTTP error {e.resp.status}: {e.error_details}")
            if e.resp.status == 403:
                print("Rate limit exceeded. Sleeping for 100 seconds.")
                time.sleep(100)
            else:
                raise

    return all_video_data


def main():
    youtube = get_authenticated_service()
    playlist_id = 'UU' + 'UCt7fwAhXDy3oNFTAzF2o8Pw'[2:]  # The Needle Drop's "Uploads" playlist ID
    start_date = "2010-03-08T00:00:00Z"
    end_date = datetime.datetime.utcnow().isoformat() + 'Z'

    # Load or initialize the checksum record
    checksum_file = 'data/checksums.txt'
    try:
        with open(checksum_file, 'r') as f:
            existing_checksums = {line.strip() for line in f}
    except FileNotFoundError:
        existing_checksums = set()

    try:
        all_video_data = get_video_data(youtube, playlist_id)

        # Filter for new videos based on checksums
        new_video_data = [video for video in all_video_data if is_video_new(video['id'], existing_checksums)]
        
        # Update the checksums file with new video IDs
        with open(checksum_file, 'a') as f:
            for video in new_video_data:
                f.write(compute_checksum(video['id']) + '\n')

    finally:
        if os.path.exists('data/cache/cache.pkl'):
            os.remove('data/cache/cache.pkl')

    os.makedirs('data/raw', exist_ok=True)
    filename = f"data/raw/video_data_{start_date}_to_{end_date}.json"

    # Save only new video data
    with open(filename, 'w') as f:
        json.dump(new_video_data, f, indent=4)

if __name__ == '__main__':
    main()
