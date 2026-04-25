# SpotiSync — TODO

## Phase 1: Project Setup
- [x] Create project folder `spotisync/`
- [x] Create `requirements.txt` with: `spotipy`, `ytmusicapi`, `python-dotenv`, `rich`
- [x] Run `pip install -r requirements.txt`
- [x] Create `.env` from `.env.example`

## Phase 2: Export Spotify Data (Manual)
- [ ] Use [Exportify](https://watsonbox.github.io/exportify/) to export Liked Songs/Playlists to CSV
- [ ] Save the CSV file as `spotify_export.csv` in the project root

## Phase 3: YT Music Auth
- [x] Run `ytmusicapi browser`
- [x] Complete browser login flow
- [x] Confirm `browser.json` saved in project root

## Phase 4: Parse Export (`parse_csv.py`)
- [x] Read `spotify_export.csv`
- [x] Extract `Track Name`, `Artist Name(s)`, `Album Name`
- [x] Return clean list of track objects

## Phase 5: YT Music Auth
- [x] Create `browser.json` from headers
- [x] Verify authentication works

## Phase 6: Sync to YT Music (`ytmusic.py`)
- [ ] Init YTMusic client with `oauth.json`
- [ ] For each song: `ytmusic.search(f"{name} {artist}", filter="songs", limit=1)`
- [ ] If result found: `ytmusic.rate_song(videoId, "LIKE")`
- [ ] Add `time.sleep(0.35)` between requests (rate limiting)
- [ ] Track success + failed songs separately

## Phase 7: CLI + Output (`main.py`)
- [ ] Wire Phase 4 → 5 → 6 together
- [ ] Add `rich` progress bars for fetch + sync phases
- [ ] Print summary table (synced / failed / total)
- [ ] Dump failed songs to `failed_songs.json`

## Phase 8: Polish
- [ ] Add `--dry-run` flag (fetch only, no write)
- [ ] Add `--retry` flag (reads `failed_songs.json`, retries only those)
- [ ] Handle edge cases: deleted tracks, region-locked songs, API timeouts
- [ ] Write `README.md`
