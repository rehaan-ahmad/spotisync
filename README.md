<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Spotify-CSV%20Export-1DB954?style=for-the-badge&logo=spotify&logoColor=white" />
  <img src="https://img.shields.io/badge/YouTube%20Music-Sync-FF0000?style=for-the-badge&logo=youtubemusic&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" />
</p>

# 🎵 SpotiSync

**Sync your Spotify liked songs and playlists to YouTube Music** — no Spotify Premium required.

SpotiSync reads a CSV export of your Spotify library (via [Exportify](https://exportify.app)) and automatically creates a matching playlist on YouTube Music, searching for each track and adding it one by one.

---

## ✨ Features

- 🎧 **No Spotify Premium needed** — uses a CSV export instead of the Spotify API
- 📋 **Creates a dedicated playlist** on YouTube Music (default: *"Spotify Liked"*)
- 🔍 **Intelligent search** — matches tracks by name + artist
- 📊 **Rich progress bar** — real-time feedback with `rich`
- ❌ **Failed song tracking** — saves unmatched songs to `failed_songs.json`
- 🔄 **Retry support** — re-run only previously failed tracks with `--retry`
- 👀 **Dry-run mode** — preview what will be synced without writing anything

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/rehaan-ahmad/spotisync.git
cd spotisync

# 2. Install dependencies
pip install -r requirements.txt

# 3. Export your Spotify library (see USAGE.md for details)
#    Save the CSV as spotify_export.csv in this folder

# 4. Set up YouTube Music authentication
ytmusicapi browser
#    → Paste request headers from music.youtube.com (see USAGE.md)

# 5. Run the sync!
python main.py
```

> 📖 **First time?** Read [`USAGE.md`](USAGE.md) for detailed step-by-step instructions.

---

## 📁 Project Structure

```
spotisync/
├── main.py              # CLI entry point (start here)
├── parse_csv.py         # Parses Exportify CSV into track objects
├── ytmusic.py           # Handles YT Music auth, playlist creation & sync
├── requirements.txt     # Python dependencies
├── USAGE.md             # Detailed usage instructions
├── TODO.md              # Development roadmap
├── .gitignore           # Files excluded from version control
└── README.md            # You are here
```

---

## 🛠️ Usage

### Basic Sync
```bash
python main.py
```
Reads `spotify_export.csv`, authenticates with `browser.json`, and syncs all tracks to the *"Spotify Liked"* playlist on YouTube Music.

### Custom CSV File
```bash
python main.py --csv my_playlist.csv
```

### Custom Playlist Name
```bash
python main.py --playlist "Road Trip 2024"
```

### Dry Run (Preview Only)
```bash
python main.py --dry-run
```
Parses the CSV and prints the first 20 tracks without syncing anything.

### Retry Failed Songs
```bash
python main.py --retry
```
Reads `failed_songs.json` from a previous run and attempts to sync only those tracks.

---

## 🔧 Dependencies

| Package | Purpose |
|---------|---------|
| [`ytmusicapi`](https://github.com/sigma67/ytmusicapi) | Unofficial YouTube Music API |
| [`rich`](https://github.com/Textualize/rich) | Beautiful terminal output & progress bars |

> **Note:** `spotipy` and `python-dotenv` are listed in `requirements.txt` for future use but are not currently required.

---

## ⚠️ Limitations

- **Browser cookies expire.** If you get `401 Unauthorized` errors, you'll need to re-export your `browser.json` headers. See [USAGE.md](USAGE.md#step-2-youtube-music-authentication).
- **Search accuracy.** YouTube Music search may occasionally return the wrong version of a song (e.g., a cover or live version). Check `failed_songs.json` for any misses.
- **Rate limiting.** The script adds a 0.5-second delay between API calls. For very large libraries (1000+ songs), the sync may take 10+ minutes.
- **No duplicate detection.** Running the script twice will add songs again. Clear the playlist first if you need a fresh sync.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/rehaan-ahmad">Rehaan Ahmad</a>
</p>
