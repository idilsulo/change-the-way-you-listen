from flask import Flask

from flask import render_template, request, redirect, session
from flask_session import Session
import time
import uuid
import pandas as pd

# import threading

from analysis import *
import arguments
args = arguments.make_parser()


os.environ['SPOTIPY_REDIRECT_URI'] = args['SPOTIPY_REDIRECT_URI']
os.environ['SPOTIPY_CLIENT_SECRET'] = args['SPOTIPY_CLIENT_SECRET']
os.environ['SPOTIPY_CLIENT_ID'] = args['SPOTIPY_CLIENT_ID']

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

sp = None
all_tracks = pd.DataFrame()
t = None

def session_cache_path():
    return caches_folder + session.get('uuid')

def convert_features(features):
    description = ""
    for feature, value in features.items():
        if int(value) < 33:
            description += "Low {} - ".format(feature)
        elif int(value) > 66:
            description += "High {} - ".format(feature)

    if len(description) > 5: 
        return description[:-2]
    else: 
        return description



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/acknowledgement')
def acknowledgement():
    return render_template('acknowledgement.html')

@app.route('/callback')
def callback():
    my_analysis()

# @app.route('/my-analysis', methods=['POST', 'GET'])
@app.route('/my-analysis')
def my_analysis():
    if not session.get('uuid'):
        # Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    scope = 'user-read-recently-played user-top-read playlist-modify-public playlist-modify-private user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                                cache_path=session_cache_path(),
                                                show_dialog=True)

    if request.args.get("code"):
        # Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/my-analysis')

    if not auth_manager.get_cached_token():
        # Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # TO-DO: Add a form to select the analysis of:
    #        * Past 4 weeks
    #        * Past 6 months
    #        * Past 3 years

    # Get the top genres of user based on top artists
    sp, user_name, top_genres_data = user_top_genres(auth_manager, term='medium_term')
    top_genres_data = top_genres_data.decode()

    # TO_DO: Get top genres in the short term
    # top_genres_st = 
    return render_template('analysis.html', user=user_name, top_genres=top_genres_data)


# @app.route('/my-playlist', methods=['POST', 'GET'])
@app.route('/my-playlist')
def my_playlist():
    if not session.get('uuid'):
        # Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    scope = 'user-read-recently-played user-top-read playlist-modify-public playlist-modify-private user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                                cache_path=session_cache_path(),
                                                show_dialog=True)

    if request.args.get("code"):
        # Being redirected from Spotify auth page
        return redirect('/my-analysis')

    if not auth_manager.get_cached_token():
        # Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    sp, top_genres, top_genres_and_artists = get_top_genres(auth_manager, term="short_term")
    top_genre = genre_selection(top_genres, 0)
    _, all_tracks, user_name = return_all_tracks(sp, top_genre, top_genres_and_artists, term="short_term")
    playlist = return_playlist(sp=sp, df=all_tracks)
    # print("Printing...")
    # print(playlist[["danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]])
    track_names, track_ids = get_playlist_tracks(sp, playlist)
    string = ""
    for i in track_ids:
        string += i
        string += " "
    return render_template('playlist.html', user=user_name, track_names=track_names, track_ids=string[:-1], 
                                            top_genre=top_genre, top_genres=list(top_genres.keys())[:3], features={})

@app.route('/customized-playlist', methods=['POST'])
def customized_playlist():

    # Return playlist features e.g: high danceability, low energy 
    #        together with playlist as a string

    features = {}
    features['danceability']     = request.form['danceability']
    features['energy']           = request.form['energy']
    features['speechiness']      = request.form['speechiness']
    features['acousticness']     = request.form['acousticness']
    features['instrumentalness'] = request.form['instrumentalness']
    features['liveness']         = request.form['liveness']
    features['valence']          = request.form['valence']
    features['tempo']            = request.form['tempo']
    
    if not session.get('uuid'):
        # Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    scope = 'user-read-recently-played user-top-read playlist-modify-public playlist-modify-private user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                                cache_path=session_cache_path(),
                                                show_dialog=True)

    if request.args.get("code"):
        # Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/my-analysis')

    if not auth_manager.get_cached_token():
        # Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    sp, top_genres, top_genres_and_artists = get_top_genres(auth_manager, term="short_term")

    print("Requested: ", request.form['genre'])
    top_genre = genre_selection(top_genres, 0, requested=request.form['genre'])
    _, all_tracks, user_name = return_all_tracks(sp, top_genre, top_genres_and_artists, term="short_term")
    playlist = return_playlist(sp=sp, df=all_tracks, features=features)
    print("Printing...")
    print(playlist[["danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]])
    track_names, track_ids = get_playlist_tracks(sp, playlist)

    string = ""
    for i in track_ids:
        string += i
        string += " "

    description = convert_features(features)
    return render_template('playlist.html', user=user_name, track_names=track_names, track_ids=string[:-1],
                                            top_genres=list(top_genres.keys())[:3], top_genre=top_genre, features=features, 
                                            description=description)

@app.route('/save-playlist', methods=['POST'])
def save_playlist():
    if not session.get('uuid'):
        # Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    scope = 'user-read-recently-played user-top-read playlist-modify-public playlist-modify-private user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                                cache_path=session_cache_path(),
                                                show_dialog=True)

    if request.args.get("code"):
        # Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/my-analysis')

    if not auth_manager.get_cached_token():
        # Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_name = sp.current_user()['display_name']
    user_id = sp.current_user()['id']
    name = request.form['playlist-name']
    tracks = request.form['tracks']
    print(tracks)

    sp.user_playlist_create(user=user_id, name=name, public=True)
    p_id = None
    for playlist in sp.user_playlists(user_id)['items']:
        print(playlist['name'])
        if playlist['name'] == name:
            p_id = playlist['id']
            break

    tracks = tracks.split(" ")
    tracks = [t[1:-1] for t in tracks]
    print(tracks)
    sp.user_playlist_add_tracks(user=user_id, playlist_id=p_id, tracks=tracks)
    return render_template('save-playlist.html', user=user_name, name=name)

if __name__ == '__main__':
    app.run(debug=True)
