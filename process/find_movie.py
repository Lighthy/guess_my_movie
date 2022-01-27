import pandas as pd
import numpy as np
import json
from process.process_data import *
from scipy.spatial import distance
import os
from django.conf import settings


def match_movies(desc_vectors, df):
    df['match'] = 0.0
    for index, movie in df.iterrows():
        movie_vectors = np.array(json.loads(movie['Plot_vectors']))
        distances = distance.cdist(desc_vectors, movie_vectors).min(axis=1)
        distances = [d if d >= 0.0001 else 0 for d in distances]
        zeros = distances.count(0) / len(distances)
        cumul_dist = sum(distances) * (1 - zeros)
        df['match'].iloc[index] = cumul_dist
    return df


def get_most_related_movie(desc, genre_csv):

    mylist = []
    for chunk in pd.read_csv(os.path.join(settings.BASE_DIR, f'polls/static/data/splited_dataset/{genre_csv}.csv'),
                             chunksize=2000):
        mylist.append(chunk)

    df = pd.concat(mylist, axis=0)
    del mylist

    nlp_en = spacy.load('en_core_web_lg')
    pd.set_option('display.max_rows', None)

    desc = remove_punctuation(desc)
    # desc = tokenize(desc)
    desc = key_words(nlp_en, desc)
    desc = abstract(desc, 2, True)
    desc_vec = vectorize(nlp_en, desc)

    movies = match_movies(desc_vec, df)
    df = None
    del df
    result = movies.sort_values(by=['match']).head(5)
    return result[['Title', 'match', 'tmdb_id', 'poster_path']]


if __name__ == '__main__':
    s = datetime.datetime.now()
    desc = "little man are on a quest to destroy a magic ring. They are helped by a wizard, an elf, a man and a dwarf. Together they fight the forces of evil."
    movies = get_most_related_movie(desc, 'Fantasy')
    print(movies)
    print(f'\n\nFinish in {datetime.datetime.now() - s}')
