import pandas as pd
from nltk.corpus import wordnet


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)

    """
    df = pd.read_csv('splited_dataset/fantasy.csv')
    df = df[df['tmdb_id'] == 26914]
    print(df[['Title', 'tmdb_id']])
    """

    df = pd.read_csv('dataset_processed.csv')
    print(df[['Title', 'Plot_key_words']])
