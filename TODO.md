# SpotiSync — Development Roadmap

All phases are complete. This file is kept for historical reference.

## Phase 1: Project Setup ✅
- [x] Create project folder and structure
- [x] Create `requirements.txt` with `ytmusicapi`, `rich`
- [x] Install dependencies

## Phase 2: Export Spotify Data ✅
- [x] Use [Exportify](https://exportify.app) to export Liked Songs to CSV
- [x] Save as `spotify_export.csv` in project root

## Phase 3: YouTube Music Authentication ✅
- [x] Run `ytmusicapi browser` or manually create `browser.json`
- [x] Verify authentication works against YT Music API

## Phase 4: CSV Parser (`parse_csv.py`) ✅
- [x] Read `spotify_export.csv`
- [x] Extract `Track Name`, `Artist Name(s)`, `Album Name`
- [x] Return clean list of track dictionaries

## Phase 5: Sync Engine (`ytmusic.py`) ✅
- [x] Initialize YTMusic client with `browser.json`
- [x] Create or find target playlist ("Spotify Liked")
- [x] Search for each track and add to playlist
- [x] Duplicate detection — skip songs already in playlist
- [x] Rate limiting with `time.sleep(0.5)`
- [x] Track success/failed songs separately

## Phase 6: CLI (`main.py`) ✅
- [x] Wire CSV parsing → YT Music sync together
- [x] Add `rich` progress bars and summary table
- [x] `--dry-run` flag (preview only)
- [x] `--retry` flag (retry from `failed_songs.json`)
- [x] `--csv`, `--playlist`, `--auth` options
- [x] Dump failed songs to `failed_songs.json`

## Phase 7: Polish ✅
- [x] Write `README.md` with badges and documentation
- [x] Write `USAGE.md` with step-by-step guide
- [x] Clean `.gitignore` for credentials and user data
- [x] Remove orphan files and unused dependencies
