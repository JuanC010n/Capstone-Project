from ast import main


def executeSearch(parameters):
  import spotipy
  from spotipy.oauth2 import SpotifyClientCredentials
  client_id = '8d151780e7f149bbb92f1916e109eef2'
  c_secret = '3bf22a6ab36c48c0b2b7d6b1ea5985f0'
  client_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=c_secret)
  sp = spotipy.Spotify(client_credentials_manager = client_credentials)

  searchResults = sp.search(q=parameters, type="track", limit = 10)
  a = searchResults.get("tracks").get("items")
  i = 0
  arrval = []
  for i in range(0,len(a)):
    arrval.append([a[i]['album']['images'][0]['url'],a[i]['artists'][0]['name'],a[i]['album']['name'],a[i]['name'],a[0]['id'],a[1]['popularity'],a[0]['album'].get("release_date")[0:4:1]])
  return arrval

