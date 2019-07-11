import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def song_search_number():
    while True:
        try:
           num_of_songs = int(input("How many songs do you want to include in your search? \n"))
           return num_of_songs
        except ValueError:
           print("That's not a number! Try again.")
           continue
        else:
           break

list_of_songs = {}
def song_inputs():

    num_of_songs = song_search_number()
    if num_of_songs > 0:
        for x in range(num_of_songs):
            if x == 0:
                song = input("What's the 1st song called?").lower()
                artist = input("Who's it by?").lower()
                list_of_songs[song] = artist
            elif x == 1:
                song = input("What's the 2nd song called?").lower()
                artist = input("Who's it by?").lower()
                list_of_songs[song] = artist
            elif x == 2:
                song = input("What's the 3rd song called?").lower()
                artist = input("Who's it by?").lower()
                list_of_songs[song] = artist
            else:
                song = input(f"What's the {x+1}th song called?").lower()
                artist = input("Who's it by?").lower()
                list_of_songs[song] = artist



def search_for_playlists():
    playlist_ids = []
    for song in list_of_songs:
        search_str = song
        playlist = sp.search(search_str, limit=3, type='playlist')
        for item in playlist['playlists']['items']:
            playlist_ids.append(item['uri'])
    return playlist_ids


def get_matching_playlists():
    song_inputs()
    playlist_ids = search_for_playlists()
    good_playlists = []
    count = 0
    for uri in playlist_ids:
        count += 1
        print(f"Playlist count: {count}/{len(playlist_ids)}")
        track_names = {}
        songs_remaining = len(list_of_songs)
        ids = []

        playlist_data = sp.user_playlist_tracks(uri.split(':')[0], uri.split(':')[2])
        playlist_data_items = playlist_data['items']

        while playlist_data['next']:
            playlist_data = sp.next(playlist_data)
            playlist_data_items.extend(playlist_data['items'])

        for item in playlist_data['items']:
            track = item['track']
            ids.append(track['id'])
        print(f"Playlist length: {len(ids)}")
        for id in ids:
            meta = sp.track(id)
            name = meta['name'].lower()
            artist = meta['album']['artists'][0]['name'].lower()

            if " (" in name:
                name = name.split(" (")[0]
            if name in list_of_songs:
                if list_of_songs[name] == artist:
                    songs_remaining -= 1
                    if songs_remaining == 0:
                        good_playlists.append(uri)
                        break
    print(good_playlists)

get_matching_playlists()



#   Loops to ensure I get every track of the playlist
   # while results['next']:
   #     results = sp.next(results)
   #     tracks.extend(results['items']["track"]["name"])

#print (json.dumps(tracks[0]))
