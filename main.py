from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

SPOTIFY_CLIENT_ID = "d4f1fd6f059240a3a95aa588dc489380"
SPOTIFY_CLIENT_SECRET = "a85ca9f792904cf6a9ddd1b954202c56"
REDIRECT_URI = "http://example.com"

# Create a Spotify API Client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username="ma100",  # email might also work, I haven't tested it
    )
)

user = sp.current_user()
user_id = user["id"]

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}/")

soup = BeautifulSoup(response.text, "html.parser")
song_names = soup.find_all(name="h3", id="title-of-a-story", class_="lrv-u-font-size-16")
song_names_clean = [song.getText().strip("\n" "\t") for song in song_names]
print(song_names_clean)

class_artist = "a-truncate-ellipsis-2line"
song_artists = soup.find_all(name="span", class_=class_artist)
song_artists_clean = [artist.getText().strip("\n" "\t") for artist in song_artists]
print(song_artists_clean)

#Convert the artists and songs into a dictionary
playlist = {song_artists_clean[i] : song_names_clean[i] for i in range(len(song_artists_clean))}

#Create a playlist of song uris
final_playlist_uris = []
for i in range(0, len(playlist)-1):
    try:
        query = f'artist:{list(playlist.keys())[i]} track:{list(playlist.values())[i]}'
        result = sp.search(q=query, limit=1, type='track')
        song_uri = result['tracks']['items'][0]['uri']
        final_playlist_uris.append(song_uri)
        print(song_uri)
    except IndexError:
        try:
            query = f'track:{list(playlist.values())[i]} year:{user_date[0:4]}'
            result = sp.search(q=query, limit=1, type='track')
            song_uri = result['tracks']['items'][0]['uri']
            final_playlist_uris.append(song_uri)
            print(song_uri)
        except IndexError:
            query = f'artist:{list(playlist.keys())[i]} track:{list(playlist.values())[i]}'
            print(f"{query} not available or not found.")

print(final_playlist_uris)

#Testing it out on one song
# query = f'track:{list(playlist.values())[9]} year:{user_date[0:4]}'
# print(query)
# result = sp.search(q=query, limit=1, type='track')
# result = json.dumps(result) #This is for the json viewer
# print(result)
#song_uri = result['tracks']['items'][0]['uri']
#print(song_uri)

#Creating the playlist
playlist_name = f"Billboard Hot 100 on {user_date}"
bb_playlist = sp.user_playlist_create(user_id,
                        playlist_name,
                        public=False,
                        collaborative=False,
                        description="100 Days of Code Billboard to Spotify Project")

bb_playlist_id = bb_playlist["id"]

sp.playlist_add_items(bb_playlist_id, final_playlist_uris, position=None)
