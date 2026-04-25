import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

def test_spotify_auth():
    scope = "user-library-read playlist-read-private"
    
    # Spotipy looks for SPOTIPY_ prefix by default. 
    # If the user used SPOTIFY_, we'll map them.
    client_id = os.getenv("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI") or os.getenv("SPOTIFY_REDIRECT_URI")
    
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope
        ))
        user = sp.current_user()
        print(f"✅ Successfully authenticated as: {user['display_name']} ({user['id']})")
        
        # Test fetching a few liked songs
        results = sp.current_user_saved_tracks(limit=1)
        print(f"✅ Successfully fetched liked songs. Total tracks: {results['total']}")
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")

if __name__ == "__main__":
    test_spotify_auth()
