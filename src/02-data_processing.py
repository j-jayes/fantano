import json
import os
import hashlib
import re

# Define the directory paths
raw_data_dir = 'data/raw/'
processed_data_dir = 'data/processed/'

# Regular expression patterns for score extraction
adjective_score_pattern = re.compile(
    r"\b(light|decent|strong)\s(\d+(\.\d+)?/10)\b",
    re.IGNORECASE
)

simple_score_pattern = re.compile(
    r"(?<!\S)(\d+(\.\d+)?/10)(?!\S)"
)

# Function to compute the checksum for a video ID
def compute_checksum(video_id):
    return hashlib.sha256(video_id.encode()).hexdigest()

# Function to check if the video is new based on checksum
def is_video_new(video_id, checksum_record):
    checksum = compute_checksum(video_id)
    return checksum not in checksum_record

# Function to process a single JSON file
def process_video_file(file_path, checksum_record):
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        video_data = json.load(file)

    # Apply filtering and score extraction
    processed_videos = []
    for video in video_data:
        video_id = video['id']
        title = video['snippet']['title'].lower()
        description = video['snippet']['description']
        # Filter for "album review" in the title and check if the video is new
        if "album review" in title and is_video_new(video_id, checksum_record):
            # Find all scores in the description
            scores = find_all_scores(description)
            # Add scores to the video data
            video['album_score'] = scores
            processed_videos.append(video)
            # Update the checksum record
            checksum_record.add(compute_checksum(video_id))

    return processed_videos

# Function to save processed data to a file
def save_processed_data(data, original_file_name):
    # Create a processed file name based on the original one
    base_name = os.path.basename(original_file_name)
    name, ext = os.path.splitext(base_name)
    processed_file_name = f"{name}_processed{ext}"
    processed_file_path = os.path.join(processed_data_dir, processed_file_name)

    # Save the processed data to the file
    with open(processed_file_path, 'w') as file:
        json.dump(data, file, indent=2)

    return processed_file_path

# Main processing function
def main():
    # Load or initialize the checksum record
    checksum_file = 'data/checksums.txt'
    try:
        with open(checksum_file, 'r') as f:
            existing_checksums = {line.strip() for line in f}
    except FileNotFoundError:
        existing_checksums = set()

    # Ensure the processed data directory exists
    os.makedirs(processed_data_dir, exist_ok=True)

    # Process all files in the raw data directory
    for filename in os.listdir(raw_data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(raw_data_dir, filename)
            processed_videos = process_video_file(file_path, existing_checksums)
            save_processed_data(processed_videos, file_path)

    # Save the updated checksum record
    with open(checksum_file, 'w') as f:
        for checksum in existing_checksums:
            f.write(checksum + '\n')

# Function to search for both patterns in the description and return matches
def find_all_scores(description):
    adjective_scores = adjective_score_pattern.findall(description)
    simple_scores = simple_score_pattern.findall(description)
    # Flatten the tuple results and merge
    return [score[1] for score in adjective_scores] + [score[0] for score in simple_scores]

if __name__ == '__main__':
    main()
