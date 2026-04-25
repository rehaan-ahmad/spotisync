from ytmusicapi import YTMusic
import os

def test_ytmusic_auth():
    if not os.path.exists("browser.json"):
        print("❌ Error: browser.json not found.")
        return

    try:
        import json
        with open("browser.json", "r") as f:
            headers = json.load(f)
        
        yt = YTMusic(auth=headers)
        # Try to fetch something that requires auth
        library = yt.get_library_playlists(limit=1)
        print("✅ Successfully authenticated with YouTube Music!")
        print(f"✅ Found library content. Authentication is working.")
    except Exception as e:
        print(f"❌ YouTube Music authentication failed: {e}")

if __name__ == "__main__":
    test_ytmusic_auth()
