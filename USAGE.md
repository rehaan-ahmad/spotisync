# 📖 SpotiSync — Usage Guide

This document walks you through the entire process of syncing your Spotify library to YouTube Music, from start to finish.

---

## Prerequisites

- **Python 3.10+** installed on your system
- A **Spotify** account (free or premium)
- A **YouTube Music / Google** account
- A modern web browser (Chrome, Edge, or Firefox)

---

## Step 1: Export Your Spotify Library

Since the Spotify API now requires a Premium account for personal library access, we use **Exportify** — a free, open-source web tool — to download your library as a CSV file.

### 1.1 Open Exportify

Visit **[https://exportify.app](https://exportify.app)** in your browser.

### 1.2 Log In to Spotify

Click **"Get Started"** and authorize Exportify to read your Spotify account. This is safe — it only requests read-only access.

### 1.3 Export Your Playlist

You'll see a list of all your playlists, including **"Liked Songs"**.

- Click the **"Export"** button next to whichever playlist you want to sync.
- A `.csv` file will be downloaded to your computer.

### 1.4 Save the CSV

Move or copy the downloaded CSV file into the `spotisync/` project folder and rename it to:

```
spotify_export.csv
```

> **Tip:** You can use any filename — just pass it with `--csv your_file.csv` when running the script.

---

## Step 2: YouTube Music Authentication

SpotiSync needs your YouTube Music session cookies to interact with your account. This is done by copying request headers from your browser's Developer Tools.

### 2.1 Open YouTube Music

Go to **[https://music.youtube.com](https://music.youtube.com)** and make sure you are **logged in**.

### 2.2 Open Developer Tools

- Press **`F12`** (or **`Ctrl + Shift + I`** on Linux/Windows, **`Cmd + Option + I`** on Mac)
- Click the **"Network"** tab

### 2.3 Capture a Request

1. Click on any playlist or navigate around the page to trigger network requests.
2. In the Network tab's filter box, type **`browse`** to find a relevant request.
3. Click on the request named `browse`.
4. In the right panel, find the **"Request Headers"** section.

### 2.4 Copy the Headers

#### Option A: Use the `ytmusicapi` CLI (Recommended)

Run this command in your terminal:

```bash
ytmusicapi browser
```

It will ask you to paste the request headers. In your browser:
- **Firefox:** Right-click the request → "Copy" → "Copy Request Headers"
- **Chrome/Edge:** Select and copy the entire "Request Headers" block manually

Paste the headers into the terminal and press **`Ctrl+D`** to save.

> ⚠️ **Chrome/Edge users:** The headers may paste in a two-line format (name on one line, value on the next). If `ytmusicapi` gives an error about missing `cookie` or `x-goog-authuser`, use **Option B** instead.

#### Option B: Create `browser.json` Manually

If the CLI doesn't work, create a file called `browser.json` in the project folder with this structure:

```json
{
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Authorization": "SAPISIDHASH ...",
    "Cookie": "VISITOR_INFO1_LIVE=...; LOGIN_INFO=...; SID=...; ...",
    "x-goog-authuser": "0",
    "x-goog-visitor-id": "...",
    "Origin": "https://music.youtube.com",
    "Referer": "https://music.youtube.com/",
    "X-Youtube-Client-Name": "67",
    "X-Youtube-Client-Version": "1.20260421.03.01"
}
```

Fill in the values from the request headers you see in your browser's Developer Tools. The most critical fields are:
- **`Cookie`** — your full session cookie string
- **`Authorization`** — the `SAPISIDHASH` value
- **`x-goog-authuser`** — usually `"0"`

### 2.5 Verify Authentication

Test that the auth file works:

```bash
python -c "from ytmusicapi import YTMusic; import json; yt = YTMusic(auth=json.load(open('browser.json'))); print('✅ Auth works!' if yt.get_library_playlists(limit=1) else '❌ Failed')"
```

> ⚠️ **Cookies expire!** If you get `401 Unauthorized` errors later, repeat this step to get fresh headers.

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `ytmusicapi` — YouTube Music API client
- `rich` — Beautiful terminal progress bars
- `spotipy` — (Reserved for future Spotify API integration)
- `python-dotenv` — (Reserved for future `.env` support)

---

## Step 4: Run the Sync

### Basic Usage

```bash
python main.py
```

This will:
1. Parse `spotify_export.csv`
2. Create a playlist called **"Spotify Liked"** on YouTube Music (or find it if it exists)
3. Search for each song and add it to the playlist
4. Show a progress bar and summary table

### Custom Options

| Flag | Description | Example |
|------|-------------|---------|
| `--csv FILE` | Use a different CSV file | `python main.py --csv rock_playlist.csv` |
| `--playlist NAME` | Set a custom YT Music playlist name | `python main.py --playlist "Chill Vibes"` |
| `--dry-run` | Preview tracks without syncing | `python main.py --dry-run` |
| `--retry` | Retry failed songs from last run | `python main.py --retry` |
| `--auth FILE` | Use a different auth file | `python main.py --auth my_auth.json` |

### Example: Sync a Specific Playlist

```bash
python main.py --csv "Road Trip 2024.csv" --playlist "Road Trip 2024"
```

---

## Step 5: Review Results

After the sync completes, you'll see a summary table:

```
         Sync Summary
┌─────────────────────┬───────┐
│ Status              │ Count │
├─────────────────────┼───────┤
│ Total Tracks        │   577 │
│ Successfully Synced │   570 │
│ Failed / Not Found  │     7 │
└─────────────────────┴───────┘
```

If any tracks failed, they are saved to **`failed_songs.json`**. You can retry them:

```bash
python main.py --retry
```

---

## 🔄 Re-running the Sync

- **Duplicate detection is automatic.** Running the script multiple times will only add songs that aren't already in the playlist.
- If you want a fresh sync, delete the playlist on YouTube Music first, then re-run.
- If your cookies have expired, re-export `browser.json` (Step 2).

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `401 Unauthorized` | Your cookies expired. Re-export `browser.json` (Step 2). |
| `No results found` for many songs | Some songs may not exist on YouTube Music (regional restrictions, indie artists). Check `failed_songs.json`. |
| `select` module error | Don't name any file `select.py` — it conflicts with Python's built-in `select` module. |
| `oauth JSON provided but oauth_credentials not provided` | Your `browser.json` is missing the `Authorization` header. Make sure to include the `SAPISIDHASH` value. |
| Script runs very slowly | The 0.5s delay between requests is intentional to avoid rate limiting. For 500 songs, expect ~5 minutes. |
