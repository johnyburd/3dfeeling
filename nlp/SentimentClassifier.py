import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
import math
import dill as pickle
import os






"""
    Returns an emotion value based on a valence and arousal score.
"""
def categorizeSentiment(v, a):
    sent = ""
    if v <= 0 and a <= 0:
        sent = "sad"
    if v <= 0 and a > 0:
        sent = "angry"
    if v > 0 and a <= 0:
        sent = "calm"
    if v > 0 and a > 0:
        sent = "happy"
    return sent

def sentenceToFeatures(sentence):
    lem = WordNetLemmatizer()
    txt = []
    for word in nltk.word_tokenize(sentence):
        word = word.lower()
        word = lem.lemmatize(word, "v")
        if word not in stopwords.words("english"):
            txt.append(word)
            # Would be time efficent to add words to dictionary here,
            # but to keep this function more general I will not.
            # dictionary.add(word)
    return txt

"""
    Categorizes sentiment into more than the four most basic categories.
"""
def categorizeSentimentcomplex(v, a):
    sentiment = ""
    angle = math.atan2(v, a)
    pi = math.pi
    if(0 <= angle < pi /8):
        sentiment = "pleased"
    if(pi / 8 <= angle < pi / 4):
        sentiment = "happy"
    if(pi / 4 <= angle < pi / 3):
        sentiment = "delighted"
    if(pi / 3 <= angle < pi / 2):
        sentiment = "excited"
    if(angle == pi /2):
        sentiment = "astonished"
    if(pi / 2 < angle < 2 * pi / 3):
        sentiment = "alarmed"
    if(2 * pi /3 <= angle < 3 * pi / 4):
        sentiment = "mad"
    if(3 * pi / 4 <= angle < 5 * pi / 6):
        sentiment = "angry"
    if(5 * pi / 6 <= angle < pi):
        sentiment = "annoyed"
    if(pi <= angle < 7 * pi / 6):
        sentiment = "miserable"
    if(7 * pi / 6 <= angle < 5 * pi / 4):
        sentiment = "depressed"
    if(5 * pi /4 <= angle > 4 * pi / 3):
        sentiment = "bored"
    if(4 * pi / 3 <= angle < 3 * pi / 2):
        sentiment = "tired"
    if(3 * pi / 2 <= angle < 5 * pi / 3):
        sentiment = "sleepy"
    if(5 * pi / 3 <= angle < 7 * pi /4):
        sentiment = "relaxed"
    if(7 * pi / 4 <= angle < 11 * pi / 6):
        sentiment = "calm"
    if(11 * pi / 6 <= angle < 0):
        sentiment = "content"
    #machine learning is just if statements
    return sentiment

def read_data():
    print("Reading data...")
    # The emobank dataset contains text entries scored for valence, arousal, and dominance.
    eb = pd.read_csv('emobank.csv', index_col=0)

    # Data is read out of emobank and stored, in a useful way in vad_docs (txt,v,a,d)
    vad_docs = []

    #read emobank
    for index, row in eb.iterrows():
        v = float(row["V"])
        a = float(row["A"])
        d = float(row["D"])
        text = row["text"]
        # transform VAD values from 6 pt positive scale to range[0, 1]
        v = v / 6
        a = a / 6
        d = d / 6
        try:
            # lemmatize, remove stop words, and transform sentence to list of words to build training docs
            txt = sentenceToFeatures(text)
            vad_docs.append((txt, v,a,d))

        except:
            #pandas struggles to read certain strings...
            print("Failed to add text: ", text)

    return vad_docs

def train_classifiers(vad_docs):
    print("Building training sets...")
    # Convert list of docs to dictionary format required by nltk classifier
    valence_training_set = [({word: (True) for word in x[0]}, x[1]) for x in vad_docs]
    arousal_training_set = [({word: (True) for word in x[0]}, x[2]) for x in vad_docs]
    dominance_training_set = [({word: (True) for word in x[0]}, x[3]) for x in vad_docs]

    print("Training Valence Classifier...")
    # Train classifier using naive bayes from nltk
    valence_classifier = NaiveBayesClassifier.train(valence_training_set)

    print("Training Arousal Classifier...")
    # Train classifier using naive bayes from nltk
    arousal_classifier = NaiveBayesClassifier.train(arousal_training_set)

    print("Training Dominance Classifier...")
    # Train classifier using naive bayes from nltk
    dominance_classifier = NaiveBayesClassifier.train(dominance_training_set)

    print('done.')
    return valence_classifier, arousal_classifier, dominance_classifier




class VADClassifier:

    def __init__(self):
        self.valence_classifier, self.arousal_classifier, self.dominance_classifier = self.train()

    def train(self):
        result = ()
        if not os.path.exists('valence_nb_classifier.pkl') \
                or not os.path.exists('arousal_nb_classifier.pkl') \
                or not os.path.exists('dominance_nb_classifier.pkl'):
            # if models are not stored locally, then train classifiers
            vad_docs = read_data()
            valence_classifier, arousal_classifier, dominance_classifier = train_classifiers(vad_docs)
            result = (valence_classifier, arousal_classifier, dominance_classifier)

            # and store models locally
            print('pickling classifiers...')
            with open('valence_nb_classifier.pkl', 'wb') as fout:
                pickle.dump(valence_classifier, fout)

            with open('arousal_nb_classifier.pkl', 'wb') as fout:
                pickle.dump(arousal_classifier, fout)

            with open('dominance_nb_classifier.pkl', 'wb') as fout:
                pickle.dump(dominance_classifier, fout)

            print('done.')
        else:
            # if models are stored locally, then load in classifiers
            print('loading models...')
            with open('valence_nb_classifier.pkl', 'rb') as fin:
                valence_classifier = pickle.load(fin)
            print('1/3')

            with open('arousal_nb_classifier.pkl', 'rb') as fin:
                arousal_classifier = pickle.load(fin)
            print('2/3')

            with open('dominance_nb_classifier.pkl', 'rb') as fin:
                dominance_classifier = pickle.load(fin)
            print('3/3')
            print('done')

        return valence_classifier, arousal_classifier, dominance_classifier
            

    """
        Removes stop words, and lemmatizes words in order to remove noise from data 
        and reduce the size of the number of values trained over.
        Takes in a sentence as a string, and returns a list of words.
    """
    def sentenceToFeatures(self, sentence):
        lem = WordNetLemmatizer()
        txt = []
        for word in nltk.word_tokenize(sentence):
            word = word.lower()
            word = lem.lemmatize(word, "v")
            if word not in stopwords.words("english"):
                txt.append(word)
                # Would be time efficent to add words to dictionary here,
                # but to keep this function more general I will not.
                # dictionary.add(word)
        return txt

    def analyzeSentiment(self, sentence):
        # convert string to format readable by classifier. Lemmatizes and removes stopwords as well.
        test_data_features = {word: True for word in self.sentenceToFeatures(sentence)}
        return self.classify(test_data_features)

    def classify(self, data_features):
        v = self.classify_valence(data_features)
        a = self.classify_arousal(data_features)
        d = self.classify_dominance(data_features)
        return v,a,d

    def classify_valence(self, data_features):
        return self.valence_classifier.classify(data_features)

    def classify_arousal(self, data_features):
        return self.arousal_classifier.classify(data_features)

    def classify_dominance(self, data_features):
        return self.dominance_classifier.classify(data_features)


from nltk.tokenize import sent_tokenize

if __name__ == "__main__":
    vad = VADClassifier()

    testdata = "These are some sentences. I love writing sentences. Sometimes when I write sentences, I get sad. " \
               "I hope someday to write a sentence all on my own. Some people say that sentences are not real."

    result = []
    for sentence in sent_tokenize(testdata):
        sentiment = vad.analyzeSentiment(sentence)
        result.append(sentence + "vad" + str([x for x in sentiment]))

    print(result)