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

def get_album_tracks(album_id, artist_id):
    """Fetch tracks and their audio features of an album by its Spotify ID, and artist information"""
    try:
        tracks = []
        album_tracks = sp.album_tracks(album_id)
        artist_info = sp.artist(artist_id)
        artist_data = {
            'popularity': artist_info['popularity'],
            'followers': artist_info['followers']['total'],
            'genres': artist_info['genres'],
            'images': artist_info['images'],
            'external_urls': artist_info['external_urls'],
            'spotify_uri': artist_info['uri'],
            'spotify_url': artist_info['external_urls']['spotify']
        }
        for track in album_tracks['items']:
            track_info = {
                'name': track['name'],
                'id': track['id'],
                'audio_features': sp.audio_features(track['id'])[0]
            }
            tracks.append(track_info)
        return tracks, artist_data
    except Exception as e:
        print(f"Error fetching tracks, audio features, or artist information for album {album_id}: {e}")
        return None, None


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
                print(f"Spotify features file for video ID {video_id} already exists. Skipping.", flush=True)
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
                artist_id = album['artists'][0]['id']  # Assuming the first artist is the main artist
                # Get the tracks of the album and artist information
                tracks, artist_data = get_album_tracks(album_id, artist_id)
                if tracks is None or artist_data is None:
                    continue  # Skip to next video on error
                # Save the tracks data along with their audio features and artist information
                # to spotify_features_dir with the video ID in the filename
                album_data = {
                    'tracks': tracks,
                    'artist_info': artist_data
                }
                try:
                    with open(output_file, 'w') as outfile:
                        json.dump(album_data, outfile)
                    print(f"Saved Spotify data, audio features, and artist information for video ID {video_id} to {output_file}", flush=True)
                except Exception as e:
                    print(f"Error saving file {output_file}: {e}")
            else:
                print(f"No albums found on Spotify for search term: {title}")

if __name__ == '__main__':
    main()
