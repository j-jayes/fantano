import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_transcript(video_id):
    try:
        # Fetch the transcript using the video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Transcript for video ID {video_id} has been fetched successfully.")
        return transcript
    except TranscriptsDisabled:
        print(f"Transcript is disabled for video ID {video_id}.")
    except NoTranscriptFound:
        print(f"No transcript found for video ID {video_id}.")
    except Exception as e:
        print(f"An error occurred while fetching the transcript for video {video_id}: {e}")
    return None

def save_transcript(transcript, video_id, directory):
    try:
        # Define the filename based on the video ID
        filename = f"{directory}/{video_id}_transcript.json"
        # Save the transcript to the specified directory
        with open(filename, 'w') as file:
            json.dump(transcript, file)
        print(f"Transcript for video ID {video_id} has been saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving the transcript for video {video_id}: {e}")

def process_video_ids_from_file(file_path, transcripts_dir):
    # Load the video IDs from the JSON file
    with open(file_path, 'r') as file:
        videos_data = json.load(file)

    # Extract video IDs
    video_ids = [video['id'] for video in videos_data]

    # Loop through the video IDs and process each one
    for video_id in video_ids:
        transcript_path = f"{transcripts_dir}/{video_id}_transcript.json"
        # Check if the transcript file already exists
        if not os.path.exists(transcript_path):
            transcript = get_transcript(video_id)
            if transcript:
                save_transcript(transcript, video_id, transcripts_dir)
        else:
            print(f"Transcript for video ID {video_id} already exists at {transcript_path}.")

def main():
    # Path to the processed data directory
    processed_dir = 'data/processed'
    transcripts_dir = 'data/transcripts'

    # Ensure the target directory exists
    if not os.path.exists(transcripts_dir):
        os.makedirs(transcripts_dir)

    # Iterate through all JSON files in the processed data directory
    for file_name in os.listdir(processed_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(processed_dir, file_name)
            print(f"Processing file: {file_path}")
            process_video_ids_from_file(file_path, transcripts_dir)

if __name__ == "__main__":
    main()
