import pandas as pd
import requests
import datetime

def get_themoviedb_infos(title):
    tmdb_genres = {
        'Action': 28,
        'Adventure': 12,
        'Animation': 16,
        'Comedy': 35,
        'Crime': 80,
        'Documentary': 99,
        'Drama': 18,
        'Family': 10751,
        'Fantasy': 14,
        'History': 36,
        'Horror': 27,
        'Music': 10402,
        'Mystery': 9648,
        'Romance': 10749,
        'Science Fiction': 878,
        'TV Movie': 10770,
        'Thriller': 53,
        'War': 10752,
        'Western': 37
    }
    tmdb_genres = {v: k for k, v in tmdb_genres.items()}

    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    transform_title = ''.join(filter(whitelist.__contains__, title)).strip().replace(' ', '+').lower()

    try:
        url = f'https://api.themoviedb.org/3/search/movie?api_key=9321570217c3d0327d1dd05232b0b9c1&query={transform_title}'
        response = requests.get(url)

        response.raise_for_status()
        json_response = response.json()
        response.close()
        if len(json_response['results']) > 0:
            genres = []
            for g in json_response['results'][0]['genre_ids']:
                genres.append(tmdb_genres[g])
            return json_response['results'][0]['id'], json_response['results'][0]['poster_path'], genres
        else:
            return -1, '', []
    except:
        return -1, '', []


if __name__ == '__main__':
    df = pd.read_csv('wiki_movie_plots_deduped.csv')

    s = datetime.datetime.now()

    df['tmdb_id'], df['poster_path'], df['Genre'] = zip(*df['Title'].map(get_themoviedb_infos))
    df = df[(df['tmdb_id'] != -1) & (df['Genre'].str.len() > 0)]

    print(df[['tmdb_id', 'Genre']])

    df.to_csv('wiki_movie_plots_deduped_processed.csv', index=False)
    print(f'Finish 1000 movies in {datetime.datetime.now() - s}')
