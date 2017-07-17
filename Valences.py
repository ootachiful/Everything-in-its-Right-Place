import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import itemgetter
import csv


def get_artist_uri(artist_name):
    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    artist_dict = items[0]
    # Gets artist ID and name from dictionary
    artist_id = artist_dict['id']
    artist_uri = 'spotify:artist:' + artist_id
    return artist_uri


def get_artist_albums(artist_uri):
    album_names = []
    album_uris = []
    results = sp.artist_albums(artist_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    for album in albums:
        album_names.append(album['name'])
        album_uris.append(album['id'])
    return [list(x) for x in zip(album_names, album_uris)]


def get_album_tracks(album_uri):
    track_names = []
    track_uris = []
    results = sp.album_tracks(album_uri)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for track in tracks:
        track_names.append(track['name'])
        track_uris.append(track['id'])
    return [list(x) for x in zip(track_names, track_uris)]


def get_track_valence(track_name, track_uri):
    results = sp.audio_features(track_uri)
    if track_name == 'Trans-Atlantic Drawl':
        print(results)
    return [track_name, results[0]['valence']]


def get_track_uri_from_name(artist_name, track_name):
    results = sp.search(q='artist:' + artist_name + ' track:' + track_name, type='track')
    return [track_name, results['tracks']['items'][0]['id']]


# Authentication stuff - don't forget to remove these values before pushing
client_credentials_manager = SpotifyClientCredentials(client_id='082fd9d9299044acb10c4bde184a4364',
                                                      client_secret='df3409c9f4a14594812d63e881c63d6f')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

# It'd honestly be easier to enter all this manually but I kinda wanted more experience with APIs
# Get the artist URI based on name
radiohead_artist_uri = get_artist_uri('Radiohead')
# Get the artist albums based on artist URI
temp_album_list = get_artist_albums(radiohead_artist_uri)
# Removes the TKOL RMX, I Might Be Wrong and original OK Computer albums
to_remove = ['TKOL RMX 1234567', 'I Might Be Wrong', 'OK Computer']
radiohead_album_list = [v for v in temp_album_list if v[0] not in to_remove]
# Get the album tracks based on album URI
temp_track_list = []
for i in range(0, len(radiohead_album_list)):
    temp_track_list.extend(get_album_tracks(radiohead_album_list[i][1]))
# Adds all the b-sides that aren't part of any albums. This is really bad of me, sorry.
# Pablo Honey era
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Million Dollar Question'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Faithless the Wonder Boy'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Coke Babies'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Yes I Am'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Inside My Head'))
# The Bends era
temp_track_list.append(get_track_uri_from_name('Radiohead', 'The Trickster'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Lewis (Mistreated)'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Punchdrunk Lovesick Singalong'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Permanent Daylight'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Lozenge of Love'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'You Never Wash Up After Yourself'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'India Rubber'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'How Can You Be Sure?'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Maquiladora'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Killer Cars'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Talk Show Host'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Bishop\'s Robes'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Banana Co'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Molasses'))
# Amnesiac era
temp_track_list.append(get_track_uri_from_name('Radiohead', 'The Amazing Sounds of Orgy'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Trans-Atlantic Drawl'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Fast-Track'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Kinetic'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Cuttooth'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Worrywort'))
# A search for 'Fog' comes up with 'Fog (Again)' from Com Lag, so this needs to be added manually
temp_track_list.append(['Fog', '6XTFoFYqXJCXHNZi1yLJA9'])
# King of Limbs era
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Supercollider'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'The Butcher'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'The Daily Mail'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Staircase'))
# Moon Shaped Pol era
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Spectre'))
# Misc. era
temp_track_list.append(get_track_uri_from_name('Radiohead', 'These Are My Twisted Words'))
temp_track_list.append(get_track_uri_from_name('Radiohead', 'Harry Patch (In Memory Of)'))
# Removes all the unwanted tracks (live versions, remixes).
to_remove = ['Remyxomatosis (Cristian Vogel RMX)', 'I Will (Los Angeles Version)', '2 + 2 = 5 (Live at Earls Court)',
             'Skttrbrain (Four Tet Remix)']
radiohead_track_list = [v for v in temp_track_list if v[0] not in to_remove]
# Get the track valences based on track URI
radiohead_valence_list = []
for i in range(0, len(radiohead_track_list)):
    radiohead_valence_list.append(get_track_valence(radiohead_track_list[i][0], radiohead_track_list[i][1]))

# Sorts the track list by valence
list.sort(radiohead_valence_list, key=itemgetter(1))
# Writes the valences to a file
with open('valences.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(radiohead_valence_list)

