import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
list_of_songs = []
matching_playlists = []

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
                song = input(f"What's the {x}th song called?").lower()
                artist = input("Who's it by?").lower()
                list_of_songs[song] = artist

song_inputs()
playlist_results = []
playlist_ids = []
for song in list_of_songs:
    search_str = song[0]
    playlist = sp.search(search_str, limit=1, type='playlist')
    for item in playlist['playlists']['items']:
        playlist_ids.append(item['uri'])

print(playlist_ids)
all_track_names = []
good_playlists = []
for uri in playlist_ids[:]:
    track_names = {}
    copy_list_of_songs = list_of_songs[:]
    ids = []
    playlist_data = sp.user_playlist_tracks(uri.split(':')[0], uri.split(':')[2])
    for item in playlist_data['items']:
        track = item['track']
        ids.append(track['id'])
    for id in ids:
        meta = sp.track(id)
        name = meta['name'].lower()
        artist = meta['album']['artists'][0]['name'].lower()

        if " (" in name:
            name = name.split(" (")[0]

        if name in list_of_songs:
            del copy_list_of_songs[name]
            if len(copy_list_of_songs) == 0:
                good_playlists.append(uri)
                break
        track_names[name] = artist

    # for song in list_of_songs:
    #     if song[0] not in track_names:
    #         playlist_ids.remove(uri)
    all_track_names.append(track_names)
print(all_track_names)
print(good_playlists)



#   Loops to ensure I get every track of the playlist
   # while results['next']:
   #     results = sp.next(results)
   #     tracks.extend(results['items']["track"]["name"])

#print (json.dumps(tracks[0]))
