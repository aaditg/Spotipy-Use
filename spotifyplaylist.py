import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
REDIRECT_URI = 'http://localhost:8888/callback/'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-public"))

def create_playlist(user_id, name, description=""):

    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
    print(f"Created Playlist: {playlist['name']}")
    return playlist['id']

def search_track(query):

    result = sp.search(q=query, type='track', limit=1)
    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        print(f"Found Track: {track['name']} by {track['artists'][0]['name']}")
        return track['id']
    else:
        print("No track found.")
        return None

def add_tracks_to_playlist(playlist_id, track_ids):

    sp.playlist_add_items(playlist_id, track_ids)
    print(f"Added {len(track_ids)} tracks to playlist.")

# Main
if __name__ == "__main__":

    user_id = sp.current_user()['id']
    
    playlist_id = create_playlist(user_id, "My Custom Playlist", "This is a custom playlist created with Python!")

    track_ids = []
    for query in ["Imagine - John Lennon", "Bohemian Rhapsody - Queen", "Stairway to Heaven - Led Zeppelin"]:
        track_id = search_track(query)
        if track_id:
            track_ids.append(track_id)

    if track_ids:
        add_tracks_to_playlist(playlist_id, track_ids)
