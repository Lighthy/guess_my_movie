import pandas as pd
import datetime


if __name__ == '__main__':
    df = pd.read_csv('dataset_processed.csv')

    print(f'Dataset loaded')

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

    for k in tmdb_genres.keys():
        tmp_df = df[df['Genre'].str.contains(k)]
        tmp_df.to_csv(f'splited_dataset/{k.replace(" ", "_")}.csv', index=False)

    print(f'Datasets saved')
