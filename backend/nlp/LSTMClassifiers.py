import wordvec
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.layers import LSTM

"""
# length of lstm sequence/ number of word parts for classification.
# one integer is not necessarily equal to one integer because of fasttext
"""
MAX_LENGTH = 50


def load_emobank(path='emobank.csv'):
    """
    loads the emobank file into pandas dataframes. default path is 'emobank.csv'
    :param filename:
    :return: tuple of train, test, dev
        each contains a pandas datafram of (text, valence, arousal, dominance)
    """
    eb = pd.read_csv(path)
    train = eb[eb["split"] == "train"]
    train = (train["text"], train["V"], train["A"], train["D"])
    dev = eb[eb["split"] == "dev"]
    dev = (dev["text"], dev["V"], dev["A"], dev["D"])
    test = eb[eb["split"] == "test"]
    test = (test["text"], test["V"], test["A"], test["D"])
    return train, dev, test


def create_lstm(word_embedding_dim, max_length):
    model = Sequential()
    model.add(LSTM(max_length, input_shape=(max_length, word_embedding_dim), return_sequences=False))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def train_model(model, X, Y, epochs=30):
    model.fit(X, Y, epochs=epochs, batch_size=1, verbose=2)


def save_model(model, model_name):
    """
    saves the model to "model_name.json"
    and the weights to "model_name.hf"
    :param model:
    :param model_name:
    :return:
    """
    model_json = model.to_json()
    fn = model_name + ".json"
    with open(fn, "w") as json_file:
        json_file.write(model_json)
    fn = model_name + "_weights.hf"
    model.save_weights(fn)


def load_model(model_name):
    """
    Load model from model_name.json and model_name.hf
    :param model_name:
    :return:
    """
    fn = model_name + ".json"
    json_file = open(fn, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    fn = model_name + "_weights.hf"
    loaded_model.load_weights(fn)
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model


def load_classifiers():
    print("Loading valence classifier...")
    valence_model = load_model("./models/valence_lstm")
    print("Loading arousal classifier...")
    arousal_model = load_model("./models/arousal_lstm")
    print("Loading dominance classifier...")
    dominance_model = load_model("./models/dominance_lstm")
    print("done.")
    return valence_model, arousal_model, dominance_model


def create_and_save():

    print("Loading Emobank...")
    train, dev, test = load_emobank()
    print("done.")

    print("Embedding features...")
    # embedder = wordvec.FasttextFeatureEmbedder(wordvec_path='wiki.en/wiki.en.bin')
    embedder = wordvec.GloveFeatureEmbedder(wordvec_path="glove.twitter.27B.25d.txt")
    train_features = embedder.embed_features(train[0], MAX_LENGTH)
    word_embedding_dim = train_features.shape[2]
    print("done.")

    ###########################################################
    #                   train  models                         #
    ###########################################################

    epochs = 5

    print("Training valence model...")
    valence_model = create_lstm(word_embedding_dim, MAX_LENGTH)
    train_model(valence_model, train_features, train[1], epochs=epochs)
    print("done.")

    print("Training arousal model...")
    arousal_model = create_lstm(word_embedding_dim, MAX_LENGTH)
    train_model(arousal_model, train_features, train[1], epochs=epochs)
    print("done.")

    print("Training dominance model...")
    dominance_model = create_lstm(word_embedding_dim, MAX_LENGTH)
    train_model(dominance_model, train_features, train[1], epochs=epochs)
    print("done.")

    ##########################################################
    #                  save models                           #
    ##########################################################

    print("Saving valence models")
    save_model(valence_model, "./models/valence_lstm")
    print("done.")

    print("Saving arousal models")
    save_model(arousal_model, "./models/arousal_lstm")
    print("done.")

    print("Saving dominance models")
    save_model(dominance_model, "./models/dominance_lstm")
    print("done.")


def mean_abs_error(pred, actual):
    diff = np.sum(np.abs(pred[-1, :] - actual))
    return diff / len(pred)


def load_and_test():
    valence_model, arousal_model, dominance_model = load_classifiers()
    test_sentence = ["Here is a fun new sentence that we can all try together."]
    print("Embedding features...")
    # embedder = wordvec.FasttextFeatureEmbedder(wordvec_path='wiki.en/wiki.en.bin')
    embedder = wordvec.GloveFeatureEmbedder(wordvec_path="glove.twitter.27B.25d.txt")
    test_feats = embedder.embed_features(test_sentence, MAX_LENGTH)
    print("done.")
    v = valence_model.predict(test_feats)
    a = arousal_model.predict(test_feats)
    d = dominance_model.predict(test_feats)
    print(test_sentence)
    print("valence: ", v)
    print("arousal: ", a)
    print("dominance: ", d)

    print("Loading Emobank...")
    train, dev, test = load_emobank()
    print("Embedding features...")
    test_features = embedder.embed_features(test[0], MAX_LENGTH)
    v_preds = valence_model.predict(test_features)
    a_preds = arousal_model.predict(test_features)
    d_preds = dominance_model.predict(test_features)

    print("done.")
    print("done.")
    print("average error: ",
          mean_abs_error(v_preds, test[1]),
          mean_abs_error(a_preds, test[2]),
          mean_abs_error(d_preds, test[3]))


def mem_test():
    valence_model, arousal_model, dominance_model = load_classifiers()
    test_sentence = ["Here is a fun new sentence",
                     "This is another sentence, but it kind of sucks",
                     "I don't know why we bother witht his sentence",
                     "This sentence is alright"]

    print("Embedding features...")
    # embedder = wordvec.FasttextFeatureEmbedder(wordvec_path='wiki.en/wiki.en.bin')
    embedder = wordvec.GloveFeatureEmbedder(wordvec_path="glove.twitter.27B.25d.txt")
    test_feats = embedder.embed_features(test_sentence, MAX_LENGTH)
    print("done.")
    v = valence_model.predict(test_feats)
    a = arousal_model.predict(test_feats)
    d = dominance_model.predict(test_feats)
    for i in range(len(test_sentence)):
        print(test_sentence[i])
        print("valence: ", v[i])
        print("arousal: ", a[i])
        print("dominance: ", d[i])


class LSTMClassifier:

    def __init__(self, wordvec_path="glove.twitter.27B.25d.txt"):
        """
        Loads the keras lstm models and the feature embedder object

        :param wordvec_path: 200 MB file of word embeddings pretrained by Stanford
        """
        self.feature_embedder = wordvec.GloveFeatureEmbedder(wordvec_path)
        self.max_length = MAX_LENGTH
        self.valence_model, self.arousal_model, self.dominance_model = load_classifiers()

    def predict(self, sentence_list):
        """
        Takes a list of sentences and returns a valence, arousal, and dominance values for all sentences.

        Can not be: "a sentence"
        must be: ["a sentence"]

        :param sentence_list:
        :return: tuple containing list of valence values, arousal values, and dominance values
        """
        feature_list = self.feature_embedder.embed_features(sentence_list, self.max_length)
        v = self.valence_model.predict(feature_list)
        a = self.arousal_model.predict(feature_list)
        d = self.dominance_model.predict(feature_list)
        v = (v - 1) / 4
        a = (a - 1) / 4
        d = (d - 1) / 4
        return (v, a, d)


if __name__ == "__main__":
    # create_and_save()
    # load_and_test()
    mem_test()
