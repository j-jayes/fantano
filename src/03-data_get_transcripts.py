import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def load_cache(cache_file):
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            return json.load(file)
    return {}

def save_cache(cache, cache_file):
    with open(cache_file, 'w') as file:
        json.dump(cache, file)

def get_transcript(video_id, cache, cache_file):
    if video_id in cache:
        print(f"Skipping video ID {video_id} as it's in the cache.")
        return None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Transcript for video ID {video_id} has been fetched successfully.", flush=True)
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        cache[video_id] = True
        save_cache(cache, cache_file)
        print(f"Transcript unavailable for video ID {video_id}, updating cache.")
    except Exception as e:
        print(f"An error occurred while fetching the transcript for video {video_id}: {e}")
    return None

def save_transcript(transcript, video_id, directory):
    try:
        filename = f"{directory}/{video_id}_transcript.json"
        with open(filename, 'w') as file:
            json.dump(transcript, file)
        print(f"Transcript for video ID {video_id} has been saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving the transcript for video {video_id}: {e}")

def process_video_ids_from_file(file_path, transcripts_dir, cache, cache_file):
    with open(file_path, 'r') as file:
        videos_data = json.load(file)
    video_ids = [video['id'] for video in videos_data]
    for video_id in video_ids:
        transcript_path = f"{transcripts_dir}/{video_id}_transcript.json"
        if not os.path.exists(transcript_path):
            transcript = get_transcript(video_id, cache, cache_file)
            if transcript:
                save_transcript(transcript, video_id, transcripts_dir)
        else:
            print(f"Transcript for video ID {video_id} already exists at {transcript_path}.")

def main():
    processed_dir = 'data/processed'
    transcripts_dir = 'data/transcripts'
    cache_dir = 'data/cache'
    cache_file = f"{cache_dir}/transcript_cache.json"

    if not os.path.exists(transcripts_dir):
        os.makedirs(transcripts_dir)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    cache = load_cache(cache_file)

    for file_name in os.listdir(processed_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(processed_dir, file_name)
            print(f"Processing file: {file_path}")
            process_video_ids_from_file(file_path, transcripts_dir, cache, cache_file)

if __name__ == "__main__":
    main()
