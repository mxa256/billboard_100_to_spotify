from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
REDIRECT_URI = "http://example.com"
SPOTIFY_USER_NAME = "" #your spotify username

# Create a Spotify API Client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_USER_NAME, 
    )
)

#We need to extract the user id for creating a playlist
#We can do this after we create the API client
user = sp.current_user()
user_id = user["id"]

##Getting date input for Billboard top 100 songs and make sure our date input is good
def checkdate(date):
    try:
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
    except:
        return True
    if len(date)>10 or month <= 0 or month > 12 or day <= 0 or day > 31 or year < 1950 or year > 2022 or date[4] != "-" or date[7] != "-":
        print("Invalid Input.\n")
        return True
    return False

while breaker:
    user_date = input("Which era do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    breaker = checkdate(user_date)

#Accessing billboard API
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}/")

#Using beautifulsoup to parse the html
#Getting the song names
soup = BeautifulSoup(response.text, "html.parser")
song_names = soup.find_all(name="h3", id="title-of-a-story", class_="lrv-u-font-size-16")
song_names_clean = [song.getText().strip("\n" "\t") for song in song_names]
print(song_names_clean)

#Getting the artist names
class_artist = "a-truncate-ellipsis-2line"
song_artists = soup.find_all(name="span", class_=class_artist)
song_artists_clean = [artist.getText().strip("\n" "\t") for artist in song_artists]
print(song_artists_clean)

#Convert the artists and songs into a dictionary
playlist = {song_artists_clean[i] : song_names_clean[i] for i in range(len(song_artists_clean))}

#Create a playlist of song uris -- these are unique song identifiers that will be used to create the playlist
#Note that some songs aren't available on Spotify or cannot be found
#We query by song and artist name, if that doesn't work we query by song and year

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

#Creating the playlist
playlist_name = f"Billboard Hot 100 on {user_date}"
bb_playlist = sp.user_playlist_create(user_id,
                        playlist_name,
                        public=False,
                        collaborative=False,
                        description="100 Days of Code Billboard to Spotify Project")

#Getting the unique playlist id
bb_playlist_id = bb_playlist["id"]

#Add the extracted uris to the playlist
sp.playlist_add_items(bb_playlist_id, final_playlist_uris, position=None)

#Voila!
