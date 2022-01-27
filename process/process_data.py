import pandas as pd
import string
import nltk
import re
import spacy
from nltk.corpus import wordnet
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import datetime


auto_abstractor = AutoAbstractor()
auto_abstractor.tokenizable_doc = SimpleTokenizer()
auto_abstractor.delimiter_list = [".", "\n"]
abstractable_doc = TopNRankAbstractor()


def read_dataset(max_rows=None):
    dataset = pd.read_csv('wiki_movie_plots_deduped_processed.csv', nrows=max_rows)
    dataset = dataset[dataset['Genre'].str.contains('Fantasy')]
    return dataset


def summarize(text):
    if len(text) < 1000:
        return text
    result = ""
    result_dict = auto_abstractor.summarize(text, abstractable_doc)
    for sentence in result_dict["summarize_result"]:
        result += sentence.strip()
    return result


def remove_punctuation(text):
    no_punct = [words for words in text if words not in string.punctuation]
    words_wo_punct = ''.join(no_punct)
    return words_wo_punct


def remove_stopwords(text):
    stopword = nltk.corpus.stopwords.words('english')
    text_cleaned = [word for word in text if word not in stopword]
    return text_cleaned


def tokenize(text):
    split = re.split("\W+", text)
    return split


def vectorize(nlp_en, plot_words):
    vectors = [list(nlp_en(word).vector) for word in plot_words]
    return vectors


def key_words(nlp_en, plot):
    plot_words = nlp_en(plot)
    k_words = {}
    for token in plot_words:
        if token.pos_ in ['VERB', 'NOUN', 'ADJ', 'NUM', 'PROPN']:
            # k_words.append(token.text)
            if token.text not in k_words.keys():
                k_words[token.text.lower()] = token.pos_

    # result = set()
    # result.update([k_w for k_w in k_words])
    # return list(result)
    return k_words


def abstract(plot_words, level=1, all_hypernyms=False):
    synsets = []
    for word, pos in plot_words.items():
        synsets.append(word)
        if pos[0] not in ['NUM', 'PROPN']:
            tmp_word = word
            while level > 0:
                level -= 1
                try:
                    tmp_word = wordnet.synsets(tmp_word).hypernyms()[0]
                    if all_hypernyms:
                        synsets.append(tmp_word.name().split('.')[0])
                    elif level == 0:
                        synsets.append(tmp_word.name().split('.')[0])
                except:
                    pass

    result = set()
    result.update([s for s in synsets])
    return result


def get_similiarity(nlp_en, desc, plot):
    s = 0
    for d in desc:
        token_d = nlp_en(d)
        for p in plot:
            token_p = nlp_en(p)
            if token_d.similarity(token_p) > 0.75:
                print(d, p)
                s += 1
    return s


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    df = read_dataset().reset_index()
    # df = df.sample(frac=1)
    nlp_en = spacy.load('en_core_web_lg')

    df = df.head(200)

    start = datetime.datetime.now()
    s = start
    print(f'Start at {datetime.datetime.now()}')
    # df['Plot'] = df['Plot'].apply(lambda x: summarize(x))
    print(f'Summarized in {datetime.datetime.now() - s}')
    s = datetime.datetime.now()
    df['Plot'] = df['Plot'] + ' ' + df['Title']
    df['Plot'] = df['Plot'].apply(lambda x: remove_punctuation(x))
    print(f'Ponctuation removed in {datetime.datetime.now() - s}')
    s = datetime.datetime.now()
    df['Plot_key_words'] = df['Plot'].apply(lambda x: key_words(nlp_en, x))
    print(f'Key worded in {datetime.datetime.now() - s}')

    s = datetime.datetime.now()
    # df['Plot_key_words'] = df['Plot_key_words'].apply(lambda x: abstract(x, 2, True))
    print(f'Synseted in {datetime.datetime.now() - s}')
    s = datetime.datetime.now()
    df['Plot_vectors'] = df['Plot_key_words'].apply(lambda x: vectorize(nlp_en, x))
    print(f'Vectorized in {datetime.datetime.now() - s}')
    s = datetime.datetime.now()

    df = df[['index', 'Title', 'tmdb_id', 'poster_path', 'Genre', 'Plot_vectors']]
    df.set_index('index').to_csv('dataset_processed.csv')
    print(f'Saved in {datetime.datetime.now() - s}')

    print(f'Datasets saved')
    print(f'Total in {datetime.datetime.now() - start}')
    print(f'Finish at {datetime.datetime.now()}')
