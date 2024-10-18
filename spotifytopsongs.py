import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
REDIRECT_URI = 'http://localhost:8888/callback/'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="user-library-read"))

def get_top_songs_from_playlist(playlist_id, num_tracks=100):

    results = sp.playlist_tracks(playlist_id, limit=num_tracks)
    tracks = results['items']
    top_songs = []
    
    for item in tracks:
        track = item['track']
        top_songs.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity'],
            'id': track['id'],
            'total_play_time': track['duration_ms'] / 1000
        })
    
    return top_songs

def get_top_tracks_by_artists(artist_ids, num_tracks=5):

    top_songs = []
    for artist_id in artist_ids:
        results = sp.artist_top_tracks(artist_id)
        for track in results['tracks'][:num_tracks]:
            top_songs.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity'],
                'id': track['id'],
                'total_play_time': track['duration_ms'] / 1000
            })
    return top_songs

def aggregate_top_100_songs():

    playlist_id = '37i9dQZEVXbMDoHDwVN2tF'  # Spotify's Global Top 50 playlist
    artist_ids = [
        '1dfeR4HaWDbWqFHLkxsg1d',  # Queen
        '6eUKZXaKkcviH0Ku9w2n3V',  # Ed Sheeran
        '66CXWjxzNUsdJxJ2JdwvnR',  # Ariana Grande
        '1Xyo4u8uXC1ZmMpatF05PJ',  # The Weeknd
        '3TVXtAsR1Inumwj472S9r4'   # Drake
    ]
    
    playlist_songs = get_top_songs_from_playlist(playlist_id, num_tracks=50)
    
    artist_songs = get_top_tracks_by_artists(artist_ids, num_tracks=10)
    
    all_songs = playlist_songs + artist_songs
    all_songs = sorted(all_songs, key=lambda x: x['popularity'], reverse=True)
    
    top_100_songs = all_songs[:100]
    return top_100_songs

def print_top_songs(songs):
    for i, song in enumerate(songs, 1):
        print(f"{i}. {song['name']} by {song['artist']} (Popularity: {song['popularity']})")



# Main
if __name__ == "__main__":
    top_100_songs = aggregate_top_100_songs()
    print_top_songs(top_100_songs)
