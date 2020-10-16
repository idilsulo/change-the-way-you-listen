"""
genre_scrapper.py
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def get_artist_genres(artist_name='', artist_id=''):
    if len(artist_id) > 0:
        artist = sp.artist(artist_id)
        print("Retrieving genres for %s"% (artist['name']))
        return artist['genres']
    elif len(artist_name) > 0:
        query_result = sp.search(artist_name, limit=1, type='artist')
        print("Retrieving genres for %s"% (query_result['artists']['items'][0]['name']))
        return query_result['artists']['items'][0]['genres']


if __name__ == '__main__':

	columns = ["Genre", "Micro Genre", "Artist Name", "Artist ID"]
	df = pd.DataFrame(columns=columns)
	
	genres = sp.recommendation_genre_seeds()['genres']
	
	for genre in genres:
		# Get the recommendations for each genre
		try:
			recommendations = [(track['artists'][0]['name'], track['artists'][0]['id']) for track in sp.recommendations(seed_genres=[genre], limit=100)['tracks']]
		except:
			print("Exception occurred. Waiting for connection.")
			time.sleep(1)
			recommendations = [(track['artists'][0]['name'], track['artists'][0]['id']) for track in sp.recommendations(seed_genres=[genre], limit=100)['tracks']]
		recommendations = list(set(recommendations))

		# Get the similar artists for each genre in order to span more micro genres
		for recommendation in recommendations:
			artist_name, artist_id = recommendation
			try:
				artist_genres = get_artist_genres(artist_id=artist_id)
			except:
				print("Exception occurred. Waiting for connection.")
				time.sleep(1)
				artist_genres = get_artist_genres(artist_id=artist_id)

			for artist_genre in artist_genres:
				df = df.append({'Genre': genre, 'Micro Genre': artist_genre, 
							'Artist Name': artist_name, 'Artist ID': artist_id}, ignore_index=True)

			try:
				similar_artists = [(artist['name'], artist['id']) for artist in sp.artist_related_artists(artist_id)['artists']]
			except:
				print("Exception occurred. Waiting for connection.")
				time.sleep(1)
				similar_artists = [(artist['name'], artist['id']) for artist in sp.artist_related_artists(artist_id)['artists']]

			for s_artist_name, s_artist_id in similar_artists:
				try:
					s_artist_genres = get_artist_genres(artist_id=s_artist_id)
				except:
					print("Exception occurred. Waiting for connection.")
					time.sleep(1)
					s_artist_genres = get_artist_genres(artist_id=s_artist_id)

				for s_artist_genre in s_artist_genres:
					df = df.append({'Genre': genre, 'Micro Genre': s_artist_genre, 
								'Artist Name': s_artist_name, 'Artist ID': s_artist_id}, ignore_index=True)

		
		print(df)
		df.drop_duplicates(subset=['Genre', 'Micro Genre', 'Artist Name', 'Artist ID'], keep='first')
		df.to_csv('genres.csv')

