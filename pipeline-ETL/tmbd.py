import pandas as pd
import requests
import config

#create an external file called "config.py" to add your api key
API_KEY = config.api_key
response_list = []


for movie_id in range(550, 556):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
    r = requests.get(url)
    response_list.append(r)