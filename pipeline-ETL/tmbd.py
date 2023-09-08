import pandas as pd
import requests
import config

# create an external file called "config.py" to add your api key
API_KEY = config.api_key
response_list = []

# Extract
for movie_id in range(550, 556):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
    r = requests.get(url)
    response_list.append(r.json())

df = pd.DataFrame.from_dict(response_list)

# Transform

# Adjust genres
print(df['genres'].head())

genres_list = df['genres'].tolist()
flat_list = [item for sublist in genres_list for item in sublist]

result = []
for sublist in genres_list:
    r = []
    for item in sublist:
        r.append(item['name'])
    result.append(r)
df = df.assign(genres_all=result)

df_genres = pd.DataFrame.from_records(flat_list).drop_duplicates()

print(df_genres.head())

df_columns = ['budget', 'genres', 'id', 'imdb_id', 'original_title', 'release_date', 'revenue', 'runtime']
df_genres_column = df_genres['name'].tolist()
df.columns.extend(df_genres_column)

s = df['genres_all'].explode()
df = df.join(pd.crosstab(s.index, s))

# Adjust dates 
df['release_date'] = pd.to_datetime(df['release_date'])
df['day'] = df['release_date'].dt.day
df['month'] = df['release_date'].dt.month
df['year'] = df['release_date'].dt.year
df['day_of_week'] = df['release_date'].dt.day_name()
df_time_columns = ['id', 'release_date', 'day', 'month', 'year', 'day_of_week']

# Load
df[df_columns].to_csv('tmdb_movies.csv', index=False)
df_genres.to_csv('tmdb_genres.csv', index=False)
df[df_time_columns].to_csv('tmdb_datetimes.csv', index=False)