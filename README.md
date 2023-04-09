# Change The Way You Listen 

 
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

<div align="center">
 <a href="https://www.ismir2020.net/hamr/">ISMIR 2020</a> | <a href="http://www.changethewayyoulisten.com/">Website</a> 
</div>

 
Change The Way You Listen helps you create playlists based on your top listened artists in the last month using certain tracks properties such as danceability, energy, tempo and so on. It also shows you your own personal listening analysis based on the top artists that you had listened in the past 6 months. 

<div class='tableauPlaceholder' id='viz1605884782844' style='position: relative'><noscript><a href='http:&#47;&#47;www.changethewayyoulisten.com&#47;'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Mu&#47;MusicGenres_16027827073270&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='MusicGenres_16027827073270&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Mu&#47;MusicGenres_16027827073270&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en' /></object></div>


## Setup 

This project supports Python 3.7+. Follow the steps provided below, to setup and run this repository locally.

**Step 1:** Generate [Spotify Client ID & Secret Key](https://developer.spotify.com/dashboard/login)

After creating the credentials to use Spotify API, provide the Client ID & Secret inside `web-app/config.ini` under `[DEV]` section.

**Step 2:** Install dependencies

To run this repo, simply create a pip environment and install requirements:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage 
In order to run the web app locally, provide the following command:
```
python3 app.py
```

This will start a Flask web application in debug mode that runs on `port 5000` by default. Navigate to the following address on your browser to try it out:

```
http://localhost:5000/
```


## FAQ 

###  Why do you need a personal listening report?
Listening music is fun, but listening "content-aware" music is much more fun. Life is too short to try to search for the genre of each artist you had been listening. Using you personal listening analysis, you can explore which genres are associated with the sounds that you had been listening the most during a specific time period. This will help you explore more specific categories of the sounds when people ask you your favorite type of music. Because simply saying rock, pop or rap may not be describing your favorites in-depth. Here yoou can find a variety of ways to describe these sounds.

### Why not just listen Daily Mix playlists?
Daily Mix playlists are great but they do not allow you to use the features of tracks. When you like an artist, you do not necessarily like all the songs that they do. Maybe you do not like the "danceable" songs of that artist because you have found their new release to be not reflecting them pretty well. Using the playlist creation feature, you can decide which types of songs you want to listen in that genre corresponding to the artist you like.