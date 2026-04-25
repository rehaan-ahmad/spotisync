#!/usr/bin/env python3
"""
SpotiSync — Sync your Spotify library to YouTube Music.

Usage:
    python main.py                          Sync spotify_export.csv → YT Music playlist
    python main.py --csv my_playlist.csv    Use a custom CSV file
    python main.py --playlist "My Mix"      Set a custom playlist name on YT Music
    python main.py --dry-run                Parse CSV only, don't sync
    python main.py --retry                  Retry previously failed songs
"""

import argparse
import json
import os
import sys

from parse_csv import parse_spotify_csv
from ytmusic import sync_to_ytmusic
from rich.console import Console

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="spotisync",
        description="Sync your Spotify liked songs & playlists to YouTube Music.",
    )
    parser.add_argument(
        "--csv",
        default="spotify_export.csv",
        help="Path to the Exportify CSV file (default: spotify_export.csv)",
    )
    parser.add_argument(
        "--auth",
        default="browser.json",
        help="Path to YT Music browser auth file (default: browser.json)",
    )
    parser.add_argument(
        "--playlist",
        default="Spotify Liked",
        help='Name of the YT Music playlist to create/append to (default: "Spotify Liked")',
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse CSV and show tracks without syncing",
    )
    parser.add_argument(
        "--retry",
        action="store_true",
        help="Retry previously failed songs from failed_songs.json",
    )

    args = parser.parse_args()

    # ── Dry-run mode ──────────────────────────────────────────────
    if args.dry_run:
        tracks = parse_spotify_csv(args.csv)
        if tracks:
            console.print(f"\n[bold cyan]📋 Dry-run: {len(tracks)} tracks found[/bold cyan]\n")
            for i, t in enumerate(tracks[:20], 1):
                console.print(f"  {i:>3}. {t['name']} — {t['artist']}")
            if len(tracks) > 20:
                console.print(f"  ... and {len(tracks) - 20} more")
        return

    # ── Retry mode ────────────────────────────────────────────────
    if args.retry:
        if not os.path.exists("failed_songs.json"):
            console.print("[bold red]❌ No failed_songs.json found. Nothing to retry.[/bold red]")
            return
        with open("failed_songs.json", "r") as f:
            failed = json.load(f)
        tracks = [entry["track"] for entry in failed]
        console.print(f"[bold yellow]🔄 Retrying {len(tracks)} previously failed tracks...[/bold yellow]")
        sync_to_ytmusic(
            csv_path=None,
            auth_file=args.auth,
            playlist_name=args.playlist,
            tracks_override=tracks,
        )
        return

    # ── Normal sync ───────────────────────────────────────────────
    if not os.path.exists(args.csv):
        console.print(f"[bold red]❌ CSV file not found:[/bold red] {args.csv}")
        console.print("Export your Spotify library using https://exportify.app and save the CSV here.")
        sys.exit(1)

    if not os.path.exists(args.auth):
        console.print(f"[bold red]❌ Auth file not found:[/bold red] {args.auth}")
        console.print("Run [bold]ytmusicapi browser[/bold] or see USAGE.md for setup instructions.")
        sys.exit(1)

    sync_to_ytmusic(
        csv_path=args.csv,
        auth_file=args.auth,
        playlist_name=args.playlist,
    )


if __name__ == "__main__":
    main()
