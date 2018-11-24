#!/usr/bin/env python3
# Used to access filesystem
import numpy
import os
import shutil
# Used for song file metadata (getting title, artist, album)
from tinytag import TinyTag
# Used for args
import click
import json
# Used to access spotify
import spotipy
import spotipy.util as util

def get_album_queries_from_directory(directory):
    """
    Investigate metadata of all songs in a given directory

    Input: Directory
    Output: List of song queries in format "<song_artist> <song_title>" # TODO research if this is optimal
    """
    album_queries = list()
    existing_albums = set()
    metadata = []
    for song_directory in os.listdir(directory):
        song_directory = os.path.join(directory, song_directory)
        for song_filename in os.listdir(song_directory):
            song_dir = os.path.join(song_directory, song_filename)
            audiofile = TinyTag.get(song_dir)
            if (audiofile.artist, audiofile.album) not in existing_albums:
                album_queries.append({'artist': audiofile.artist, 'album': audiofile.album})
            existing_albums.add((audiofile.artist, audiofile.album))
    with open('added-albums', 'w') as f:
        json.dump(album_queries, f)
    return album_queries

def query_albums_on_spotify(sp, album_queries):
    """
    Get spotify track objects from a list of song queries

    Input: List of song queries
    Output: List of spotify track objects
    """
    albums = []
    albums_not_found = []
    for album_query in album_queries:
        if album_query['album']:
            print album_query
            album_q = u"album:{}+artist:{}".format(album_query['album'],album_query['artist'])
            track = sp.search(album_q, type='album', limit=1)
            print track
            try:
                album = track["albums"]["items"][0]["uri"]
                albums.append(album)
            except:
                albums_not_found.append(album_query)
    print albums
    print albums_not_found
    print len(albums_not_found)
    print "Found {}/{} albums".format(len(albums), len(album_queries))
    return albums

def add_albums_to_spotify(sp, albums):
    """
    Add spotify tracks to spotify user's library

    Input: Spotify account & List of spotify track objects
    Output: None
    """
    for album in albums:
        albums_n = [album]
        print albums_n
        sp.current_user_saved_albums_add(albums_n)

@click.command()
@click.option('--username', '-u', required=True, type=str, help="Spotify Username")
@click.option('--directory', '-d', required=True, type=str, help="Path to songs")
def main(username, directory):
    scope = 'user-library-modify'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        album_queries = get_album_queries_from_directory(directory)
        albums = query_albums_on_spotify(sp, album_queries)
        return
        add_albums_to_spotify(sp, albums)
    print("Added {} albums to your spotify library".format(len(albums)))
    print("Done.")

if __name__ == "__main__":
    main()
