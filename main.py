from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year would you like to travel to? Type the date in this format- YYYY-MM-DD: ")
year = int(date.split("-")[0])

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=URL)
site_html = response.text

soup = BeautifulSoup(site_html, "html.parser")

all_songs = soup.find_all(name="h3", id="title-of-a-story", class_="lrv-u-font-size-16")

song_list = [song.getText().strip("\n" "\t") for song in all_songs]

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

user = sp.current_user()
user_id = user["id"]

track_ids = []

for title in song_list:
    result = sp.search(q=f"track:{title} year:{year-10}-{year}", limit=1, type="track")
    try:
        track_id = result["tracks"]["items"][0]["id"]
        track_ids.append(track_id)
    except IndexError:
        print(f"{title} not found on Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"Billboard Hot 100 {date}", public=True, description=f"Playlist of "
                                                                                                    f"Billboard's Hot"
                                                                                                    f" 100 songs on "
                                                                                                    f"{date}, "
                                                                                                    f"generated using "
                                                                                                    f"Python, "
                                                                                                    f"BeautifulSoup, "
                                                                                                    f"and Spotify for "
                                                                                                    f"Developers.")

add_items = sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)

print("Playlist generator succeeded!")
