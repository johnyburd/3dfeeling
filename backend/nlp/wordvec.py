# import fasttext as ft
import numpy as np
from keras.preprocessing import sequence
from nltk.tokenize import word_tokenize


class GloveFeatureEmbedder:

    def __init__(self, wordvec_path="glove.twitter.27B.25d.txt"):
        self.embeddings_dict = {}
        with open(wordvec_path, 'r', encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], "float32")
                self.embeddings_dict[word] = vector

    def get_word_vector(self, word):
        word = word.lower()
        if word in self.embeddings_dict:
            return self.embeddings_dict[word]
        else:
            return [0 for i in range(25)]

    def embed_features(self, text, max_length, pad_sequence=True):
        X = []
        for entry in text:
            feats = []
            for i, word in enumerate(word_tokenize(entry)):
                if i < max_length:
                    vector = self.get_word_vector(word)
                    feats.append(vector)
            X.append(feats)

        if pad_sequence:
            X = sequence.pad_sequences(X, maxlen=max_length)

        return X


class FasttextFeatureEmbedder:
    def __init__(self, wordvec_path='wiki.en/wiki.en.bin'):
        # self.vectorizer = ft.load_model(wordvec_path)
        pass

    def embed_features(self, text, max_length, pad_sequence=True):
        """
        :param text: array (not dataframe) of text entries
        :param max_length:
        :return:  list max_length lists of word vectors each word vector currently length 300
        """
        X = []

        # text = text["text"]
        for entry in text:
            feats = []
            for i, word in enumerate(word_tokenize(entry)):
                if i < max_length:
                    feats.append(self.vectorizer.get_word_vector(word))
            X.append(feats)

        if pad_sequence:
            X = sequence.pad_sequences(X, maxlen=max_length)

        return X


def main():
    # word = "banana-raisinbran"
    # model = ft.load_model('wiki.en/wiki.en.bin')
    # print(model.get_word_vector(word))
    # nearest nieghbors not available with pypi release
    # neighbors = model.get_nearest_neighbors(word)
    # vectorizer = Word_Vectorizer(path)
    # print(word, ": ", vectorizer.get_word_vec(word))
    pass


if __name__ == "__main__":
    main()
