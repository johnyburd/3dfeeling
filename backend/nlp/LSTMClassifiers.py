import wordvec
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from nltk.tokenize import word_tokenize

"""
# length of lstm sequence/ number of word parts for classification.
# one integer is not necessarily equal to one integer because of fasttext
"""
MAX_LENGTH = 25

def load_emobank(path='emobank.csv'):
    """
    loads the emobank file into pandas dataframes. default path is 'emobank.csv'
    :param filename:
    :return: tuple of train, test, dev
        each contains a pandas datafram of (text, valence, arousal, dominance)
    """
    eb = pd.read_csv(path)
    train = eb[eb["split"]=="train"]
    train = (train["text"], train["V"], train["A"], train["D"])
    dev = eb[eb["split"] == "dev"]
    dev = (dev["text"], dev["V"], dev["A"], dev["D"])
    test = eb[eb["split"] == "test"]
    test = (test["text"], test["V"], test["A"], test["D"])
    return train, dev, test


def create_lstm(word_embedding_dim, max_length):
    model = Sequential()
    model.add(LSTM(max_length, input_shape=(max_length, word_embedding_dim)))
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
    fn = model_name +  ".json"
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

def load_classifiers():
    print("Loading valence classifier...")
    valence_model = load_model("valence_lstm")
    print("Loading arousal classifier...")
    arousal_model = load_model("arousal_lstm")
    print("Loading dominance classifier...")
    dominance_model = load_model("dominance_lstm")
    print("done.")
    return valence_model, arousal_model, dominance_model

    
def main():
    
    print("Loading Emobank...")
    train, dev, test = load_emobank()
    print("done.")
    
    print("Embedding features...")
    train_features = wordvec.embed_features(train[0], MAX_LENGTH, wordvec_path='wiki.en/wiki.en.bin')
    word_embedding_dim = train_features.shape[2]
    print("done.")
    
    ###########################################################
    #                   train  models                         #
    ###########################################################
    epochs = 2

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
    save_model(valence_model, "valence_lstm")
    print("done.")

    print("Saving arousal models")
    save_model(arousal_model, "arousal_lstm")
    print("done.")

    print("Saving dominance models")
    save_model(dominance_model, "dominance_lstm")
    print("done.")


    


if __name__ == "__main__":
    main()