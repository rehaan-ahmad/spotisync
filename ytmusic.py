from ytmusicapi import YTMusic
from parse_csv import parse_spotify_csv
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.console import Console
from rich.table import Table
import time
import json
import os

console = Console()

def sync_to_ytmusic(csv_path="spotify_export.csv", auth_file="browser.json", playlist_name="Spotify Liked", tracks_override=None):
    # 1. Parse tracks
    if tracks_override:
        tracks = tracks_override
        console.print(f"✅ Using {len(tracks)} tracks provided directly")
    else:
        tracks = parse_spotify_csv(csv_path)
        if not tracks:
            return

    # 2. Init YTMusic
    try:
        with open(auth_file, 'r') as f:
            headers = json.load(f)
        yt = YTMusic(auth=headers)
    except Exception as e:
        console.print(f"[bold red]❌ Failed to initialize YouTube Music:[/bold red] {e}")
        return

    # 3. Create or find playlist
    playlist_id = None
    existing_video_ids = set()
    
    try:
        playlists = yt.get_library_playlists(limit=50)
        for p in playlists:
            if p['title'] == playlist_name:
                playlist_id = p['playlistId']
                console.print(f"[bold green]✔️ Found existing playlist:[/bold green] {playlist_name}")
                
                # Fetch existing tracks to prevent duplicates
                console.print(f"[blue]🔍 Checking existing tracks in '{playlist_name}' for duplicates...[/blue]")
                playlist_data = yt.get_playlist(playlist_id, limit=None)
                for item in playlist_data.get('tracks', []):
                    if item.get('videoId'):
                        existing_video_ids.add(item['videoId'])
                
                console.print(f"📊 Found {len(existing_video_ids)} tracks already in playlist.")
                break
        
        if not playlist_id:
            playlist_id = yt.create_playlist(playlist_name, "My liked songs synced from Spotify")
            console.print(f"[bold green]🆕 Created new playlist:[/bold green] {playlist_name}")
    except Exception as e:
        console.print(f"[bold red]❌ Error with playlist setup:[/bold red] {e}")
        return

    synced_ids = []
    skipped_count = 0
    failed = []

    console.print(f"\n[bold cyan]🚀 Starting sync of {len(tracks)} tracks to '{playlist_name}'...[/bold cyan]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        search_task = progress.add_task("[green]Searching & Syncing...", total=len(tracks))

        for track in tracks:
            query = f"{track['name']} {track['artist']}"
            progress.update(search_task, description=f"[blue]Searching:[/blue] {track['name']}")
            
            try:
                # Search for the song
                search_results = yt.search(query, filter="songs", limit=1)
                
                if search_results:
                    video_id = search_results[0]['videoId']
                    
                    # Check for duplicates
                    if video_id in existing_video_ids:
                        skipped_count += 1
                        progress.update(search_task, description=f"[yellow]Skipped (exists):[/yellow] {track['name']}")
                    else:
                        # Add to playlist
                        yt.add_playlist_items(playlist_id, [video_id])
                        synced_ids.append(video_id)
                        existing_video_ids.add(video_id) # Add to set to prevent duplicates within the same run
                        progress.update(search_task, description=f"[green]Added:[/green] {track['name']}")
                else:
                    failed.append({"track": track, "reason": "No results found"})
                    progress.update(search_task, description=f"[yellow]Not found:[/yellow] {track['name']}")
            
            except Exception as e:
                failed.append({"track": track, "reason": str(e)})
                progress.update(search_task, description=f"[red]Error:[/red] {track['name']}")
            
            # Rate limiting safety
            time.sleep(0.5)
            progress.advance(search_task)

    # 3. Final Summary
    table = Table(title="Sync Summary")
    table.add_column("Status", style="bold")
    table.add_column("Count", justify="right")
    
    table.add_row("Total Tracks", str(len(tracks)))
    table.add_row("Successfully Synced", f"[green]{len(synced_ids)}[/green]")
    table.add_row("Skipped (Duplicates)", f"[yellow]{skipped_count}[/yellow]")
    table.add_row("Failed / Not Found", f"[red]{len(failed)}[/red]")
    
    console.print("\n", table)

    # Save failures for retry
    if failed:
        with open("failed_songs.json", "w") as f:
            json.dump(failed, f, indent=4)
        console.print(f"[bold yellow]⚠️ {len(failed)} tracks failed. Details saved to failed_songs.json[/bold yellow]")

if __name__ == "__main__":
    sync_to_ytmusic()
