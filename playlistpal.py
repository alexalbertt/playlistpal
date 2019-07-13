import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import webbrowser
import client

client_credentials_manager = SpotifyClientCredentials(client_id=client.client_id, client_secret=client.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def songs_or_artists(search_type):
    while search_type != "a" and search_type != "s":
        search_type = input("Do you want to search for playlists containing artists or specific songs? (a or s) \n").lower()
    return search_type

def search_number(search_type):
    while True:
        try:
            if search_type == "s":
                num_of_songs = int(input("How many songs do you want to include in your search? \n"))
                return num_of_songs
            else:
                num_of_artists = int(input("How many artists do you want to include in your search? \n"))
                return num_of_artists
        except ValueError:
            print("That's not a number! Try again.")
            continue
        else:
            break

list_of_songs = {}
list_of_artists = []
def song_inputs(search_type):
    num_of_searches = search_number(search_type)
    if search_type == "s":
        s_or_a = "song"
    else:
        s_or_a = "artist"
    if num_of_searches > 0:
        for x in range(num_of_searches):
            if x == 0:
                first = input(f"1st {s_or_a}: \n").lower()
                list_of_artists.append(first)
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[first] = artist
            elif x == 1:
                second = input(f"2nd {s_or_a}: \n").lower()
                list_of_artists.append(second)
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[second] = artist
            elif x == 2:
                third = input(f"3rd {s_or_a}: \n").lower()
                list_of_artists.append(third)
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[third] = artist
            else:
                fourth = input(f"{x+1}th {s_or_a}: \n").lower()
                list_of_artists.append(fourth)
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[fourth] = artist



def search_for_playlists(search_type):
    playlist_ids = []
    if search_type == "s":
        search_list = list_of_songs
    else:
        search_list = list_of_artists
    for search_item in search_list:
        search_str = search_item
        playlist = sp.search(search_str, limit=5, type='playlist')
        for item in playlist['playlists']['items']:
            playlist_ids.append(item['uri'])
    return playlist_ids


def get_matching_playlists():
    search_type = songs_or_artists("")
    song_inputs(search_type)
    playlist_ids = search_for_playlists(search_type)
    good_playlists = []
    count = 0
    print(playlist_ids)
    for uri in playlist_ids:
        count += 1
        print(f"Playlist count: {count}/{len(playlist_ids)}")
        if search_type == "s":
            songs_remaining = len(list_of_songs)
        else:
            copy_list_of_artists = list_of_artists[:]
        ids = []

        playlist_data = sp.user_playlist_tracks(uri.split(':')[0], uri.split(':')[2])
        playlist_data_items = playlist_data['items']

        while playlist_data['next']:
            playlist_data = sp.next(playlist_data)
            playlist_data_items.extend(playlist_data['items'])

        for item in playlist_data_items:
            track = item['track']
            ids.append(track['id'])

        print(f"Playlist length: {len(ids)}")
        for id in ids:
            try:
                meta = sp.track(id)
                name = meta['name'].lower()
                artist = meta['album']['artists'][0]['name'].lower()

                if search_type == "s":
                    if " (" in name:
                        name = name.split(" (")[0]
                    if name in list_of_songs:
                        if list_of_songs[name] == artist:
                            songs_remaining -= 1
                            if songs_remaining == 0:
                                good_playlists.append(uri)
                                break
                else:
                    if artist in copy_list_of_artists:
                        copy_list_of_artists.remove(artist)
                        if len(copy_list_of_artists) == 0:
                            good_playlists.append(uri)
                            break
            except:
                print(uri)
                print("Unavailable song in playlist")
                pass
        print(good_playlists)
    print(good_playlists)
    for good in good_playlists:
        try:
            webbrowser.open(good)
        except:
            print("Oops, you need to have spotify open for me to open the playlists.")


get_matching_playlists()
