# SpotiSync — TODO

## Phase 1: Project Setup
- [x] Create project folder `spotisync/`
- [x] Create `requirements.txt` with: `spotipy`, `ytmusicapi`, `python-dotenv`, `rich`
- [ ] Run `pip install -r requirements.txt`
- [x] Create `.env` from `.env.example`

## Phase 2: Spotify Auth
- [ ] Go to developer.spotify.com/dashboard
- [ ] Create new app
- [ ] Copy Client ID + Client Secret → `.env`
- [ ] Add redirect URI: `http://localhost:8888/callback` in app settings
- [ ] Test auth by running spotipy with `user-library-read` scope

## Phase 3: YT Music Auth
- [ ] Run `ytmusicapi oauth`
- [ ] Complete browser login flow
- [ ] Confirm `oauth.json` saved in project root

## Phase 4: Fetch Liked Songs (`spotify.py`)
- [ ] Init Spotify client via SpotifyOAuth
- [ ] Paginate `current_user_saved_tracks()` with limit=50, offset loop
- [ ] Extract `name`, `artist`, `album` per track
- [ ] Return full list

## Phase 5: Sync to YT Music (`ytmusic.py`)
- [ ] Init YTMusic client with `oauth.json`
- [ ] For each song: `ytmusic.search(f"{name} {artist}", filter="songs", limit=1)`
- [ ] If result found: `ytmusic.rate_song(videoId, "LIKE")`
- [ ] Add `time.sleep(0.35)` between requests (rate limiting)
- [ ] Track success + failed songs separately

## Phase 6: CLI + Output (`main.py`)
- [ ] Wire Phase 4 + 5 together
- [ ] Add `rich` progress bars for fetch + sync phases
- [ ] Print summary table (synced / failed / total)
- [ ] Dump failed songs to `failed_songs.json`

## Phase 7: Polish
- [ ] Add `--dry-run` flag (fetch only, no write)
- [ ] Add `--retry` flag (reads `failed_songs.json`, retries only those)
- [ ] Handle edge cases: deleted tracks, region-locked songs, API timeouts
- [ ] Write `README.md`
