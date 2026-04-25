# SpotiSync — TODO

## Phase 1: Project Setup
- [x] Create project folder `spotisync/`
- [x] Create `requirements.txt` with: `spotipy`, `ytmusicapi`, `python-dotenv`, `rich`
- [x] Run `pip install -r requirements.txt`
- [x] Create `.env` from `.env.example`

## Phase 2: Spotify Auth
- [ ] Go to developer.spotify.com/dashboard
- [ ] Create new app
- [ ] Copy Client ID + Client Secret → `.env`
- [ ] Add redirect URI in app settings:
  - Type `https://localhost:8888/callback`
  - Press **Enter** to confirm as a tag
  - Then click **Save**
- [ ] Set in `.env`: `SPOTIFY_REDIRECT_URI=https://localhost:8888/callback`
- [ ] Test auth by running spotipy with `user-library-read playlist-read-private` scope

## Phase 3: YT Music Auth
- [ ] Run `ytmusicapi oauth`
- [ ] Complete browser login flow
- [ ] Confirm `oauth.json` saved in project root

## Phase 4: Source Selection (`select.py`)
- [ ] Init Spotify client
- [ ] Fetch liked songs count via `current_user_saved_tracks(limit=1)`
- [ ] Fetch all playlists via `current_user_playlists()`
- [ ] Extract `name`, `id`, `track count` per playlist
- [ ] Use `rich` to render an interactive numbered menu:
  ```
  What do you want to sync?

  [0] Liked Songs (623 tracks)
  [1] My Playlist — chill (45 tracks)
  [2] Road Trip 2024 (88 tracks)
  ...

  Enter number:
  ```
- [ ] Return selected source as `{ type: "liked" | "playlist", id?, name }`

## Phase 5: Fetch Tracks (`spotify.py`)
- [ ] If type is `liked`: paginate `current_user_saved_tracks()`
- [ ] If type is `playlist`: paginate `playlist_tracks(playlist_id)`
- [ ] Extract `name`, `artist`, `album` per track
- [ ] Return full list

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
