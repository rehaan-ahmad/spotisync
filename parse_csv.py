import csv
import os

def parse_spotify_csv(file_path="spotify_export.csv"):
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found. Please export your data and save it here.")
        return []

    tracks = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Exportify usually uses these headers
                name = row.get("Track Name")
                artist = row.get("Artist Name(s)")
                album = row.get("Album Name")
                
                if name and artist:
                    tracks.append({
                        "name": name,
                        "artist": artist,
                        "album": album
                    })
        
        print(f"✅ Successfully parsed {len(tracks)} tracks from {file_path}")
        return tracks
    except Exception as e:
        print(f"❌ Error parsing CSV: {e}")
        return []

if __name__ == "__main__":
    parsed_tracks = parse_spotify_csv()
    for t in parsed_tracks[:5]:
        print(f"- {t['name']} by {t['artist']}")
