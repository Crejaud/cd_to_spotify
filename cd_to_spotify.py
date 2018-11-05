#!/usr/bin/env python3
import click
import spotipy
import spotipy.util as util

def get_songs_from_cd():
    #TODO investigate metadata of song to get song name & artist
    return []

def search_cd_song_on_spotify(songs):
    tracks = []
    for song in songs:
        print("Searching song: {}".format(song))
        track = sp.search(song, limit=1)
        tracks.extend(track)
        print("Found track: {}".format(sp.search(song, limit=1)))
    return tracks

def add_tracks_to_spotify(sp, tracks):
    print("Going to add tracks: {}".format(tracks))
    sp.current_user_saved_tracks_add(tracks)

@click.command()
@click.option('--username', '-u', required=True, type=str, help="Spotify Username")
def main(username):
    scope = 'user-library-read'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        songs = get_songs_from_cd()
        tracks_from_spotify = search_songs_on_spotify(songs)
        add_tracks_to_spotify(sp, tracks)
    print("Done.")

if __name__ == "__main__":
    main()
