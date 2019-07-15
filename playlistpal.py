import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import client

# input API keys here
client_credentials_manager = SpotifyClientCredentials(client_id=client.client_id, client_secret=client.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def songs_or_artists(search_type):
    """[summary]
    Ask user to input whether search is based on songs or artists.
    [description]
    """
    while search_type != "a" and search_type != "s":
        search_type = input("Do you want to search for playlists containing artists or specific songs? (a or s) \n").lower()
    return search_type

def search_number(search_type):
        """[summary]
        Ask user for number of songs/artists they want to search with.
        [description]

        """
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
    """[summary]
    Ask user to input the songs/artists they want to search.
    [description]
    Add song to dictionary with value of artist
    Or append artist to list of artists
    """
    num_of_searches = search_number(search_type)
    if search_type == "s":
        s_or_a = "song"
    else:
        s_or_a = "artist"
    if num_of_searches > 0:
        for x in range(num_of_searches):
            if x == 0:
                first = input(f"1st {s_or_a}: \n").lower()
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[first] = artist
                else:
                    list_of_artists.append(first)
            elif x == 1:
                second = input(f"2nd {s_or_a}: \n").lower()
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[second] = artist
                else:
                    list_of_artists.append(second)
            elif x == 2:
                third = input(f"3rd {s_or_a}: \n").lower()
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[third] = artist
                else:
                    list_of_artists.append(third)
            else:
                fourth = input(f"{x+1}th {s_or_a}: \n").lower()
                if search_type == "s":
                    artist = input("Who's it by? \n").lower()
                    list_of_songs[fourth] = artist
                else:
                    list_of_artists.append(fourth)



def search_for_playlists(search_type):
    """[summary]
    Search for playlists by iterating over list of songs/artists.
    [description]
    Iterate over list and use item as search string.
    Limit search to 5 playlists per item.
    Append each playlist uri to playlist_ids.
    """
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
    """[summary]
    Check each playlist to see if it contains all the songs or artists and
    return the uri's of each playlist that meets the conditions.
    [description]
    For each playlist, get the playlist tracks using the playlist uri.
    Then, iterate over each track checking if it meets the conditions for song/artist.
    If it does, remove the found song/artist and continue.
    Stop searching playlist if all songs/artists have been found.
    Add playlist to good_playlists.
    """
    search_type = songs_or_artists("")
    song_inputs(search_type)
    playlist_ids = search_for_playlists(search_type)

    # list of playlist uri's matching conditions
    good_playlists = []

    # keep track of which playlist is being searched
    count = 0

    for uri in playlist_ids:
        count += 1
        print(f"Playlist count: {count}/{len(playlist_ids)}")

        if search_type == "s":
            songs_remaining = len(list_of_songs)
        else:
            copy_list_of_artists = list_of_artists[:]

        # retrieve first 100 track IDs in playlist
        playlist_data = sp.user_playlist_tracks(uri.split(':')[0], uri.split(':')[2])
        playlist_data_items = playlist_data['items']

        # if playlist is >100 tracks, continue retrieving track IDs
        while playlist_data['next']:
            playlist_data = sp.next(playlist_data)
            playlist_data_items.extend(playlist_data['items'])

        print(f"Playlist length: {len(playlist_data_items)}")

        # check each track
        for item in playlist_data_items:
            track = item['track']
            id = track['id']

            # get track info from ID
            try:
                meta = sp.track(id)
                name = meta['name'].lower()
                artist = meta['album']['artists'][0]['name'].lower()

                if search_type == "s":
                    # if song title features another artist, split it to get the pure title
                    if " (" in name:
                        name = name.split(" (")[0]
                    # if song in list and its by the correct artist, decrease songs_remaining
                    if name in list_of_songs:
                        if list_of_songs[name] == artist:
                            songs_remaining -= 1
                            if songs_remaining == 0:
                                good_playlists.append(uri)
                                break
                else:
                    # if artist in list, remove artist from list
                    if artist in copy_list_of_artists:
                        copy_list_of_artists.remove(artist)
                        if len(copy_list_of_artists) == 0:
                            good_playlists.append(uri)
                            break
            except:
                print(uri)
                print("Unavailable song in playlist")
                pass

    print("Here are the uri's of the playlists containing what you specified:")
    for i in good_playlists:
        print(i)
    print("Copy and paste these uri's into the Spotify search bar to view the playlist.")


if __name__ == "__main__":
    get_matching_playlists()
