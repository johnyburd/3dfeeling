import fasttext as ft
import io
from keras.preprocessing import sequence
from nltk.tokenize import word_tokenize

class WordVectorizer:

    def __init__(self, fname):
        self.model = ft.load_model(fname)


    def get_word_vec(self, word):
        return self.model.get_word_vector(word)


def embed_features(text, max_length, wordvec_path='wiki.en/wiki.en.bin'):
    """
    :param text: array (not dataframe) of text entries
    :param max_length:
    :return:  list max_length lists of word vectors each word vector currently length 300
    """
    X = []

    # Load vector representations
    vectorizer = WordVectorizer(wordvec_path)

    # text = text["text"]
    for entry in text:
        feats = []
        for i, word in enumerate(word_tokenize(entry)):
            if i < max_length:
                feats.append(vectorizer.get_word_vec(word))
        X.append(feats)

    X = sequence.pad_sequences(X, maxlen=max_length)
    return X


def main():
    word = "banana-raisinbran"
    model = ft.load_model('wiki.en/wiki.en.bin')
    print(model.get_word_vector(word))
    #nearest nieghbors not available with pypi release
    #neighbors = model.get_nearest_neighbors(word)
    #vectorizer = Word_Vectorizer(path)
    #print(word, ": ", vectorizer.get_word_vec(word))


if __name__ == "__main__":
    main()



