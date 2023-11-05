import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import glob
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Define paths
processed_dir = 'data/processed'
spotify_features_dir = 'data/spotify_features'

# Ensure the target directory exists
if not os.path.exists(spotify_features_dir):
    os.makedirs(spotify_features_dir)

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                                           client_secret=os.environ['SPOTIFY_SECRET']))

def get_album_tracks(album_id):
    """Fetch tracks of an album by its Spotify ID"""
    try:
        tracks = []
        album_tracks = sp.album_tracks(album_id)
        for track in album_tracks['items']:
            tracks.append(track)
        return tracks
    except Exception as e:
        print(f"Error fetching tracks for album {album_id}: {e}")
        return None

def main():
    # Loop through all JSON files in processed_dir
    for file_name in glob.glob(f'{processed_dir}/*.json'):
        print(f"Processing file: {file_name}")
        try:
            with open(file_name) as f:
                videos = json.load(f)
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            continue  # Skip to next file on error
        
        for video in videos:
            # Extract video ID
            video_id = video['id']
            print(f"Processing video ID: {video_id}")
            # Define the output file path
            output_file = f'{spotify_features_dir}/{video_id}.json'
            # Check if the Spotify features file already exists
            if os.path.exists(output_file):
                print(f"Spotify features file for video ID {video_id} already exists. Skipping.")
                continue  # Skip to next video if file exists
            # Modify title to remove " ALBUM REVIEW" or " album review"
            title = video['snippet']['title'].replace(" ALBUM REVIEW", "").replace(" album review", "")
            # Search Spotify for the album
            try:
                result = sp.search(title, type='album')
            except Exception as e:
                print(f"Error searching Spotify for {title}: {e}")
                continue  # Skip to next video on error
            
            if result['albums']['items']:
                album = result['albums']['items'][0]
                album_id = album['id']
                # Get the tracks of the album
                tracks = get_album_tracks(album_id)
                if tracks is None:
                    continue  # Skip to next video on error
                # Save the tracks data to spotify_features_dir with the video ID in the filename
                try:
                    with open(output_file, 'w') as outfile:
                        json.dump(tracks, outfile)
                    print(f"Saved Spotify data for video ID {video_id} to {output_file}")
                except Exception as e:
                    print(f"Error saving file {output_file}: {e}")
            else:
                print(f"No albums found on Spotify for search term: {title}")


if __name__ == '__main__':
    main()

