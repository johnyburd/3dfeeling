import NaiveBayes
import LSTMClassifiers
import math
import nltk
from nltk.tokenize import sent_tokenize


def categorizeSentiment(v, a):
    """
    Returns an emotion value based on a valence and arousal score.
    """
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


def categorizeSentimentcomplex(v, a):
    """
    Categorizes sentiment into more than the four most basic categories.
    """
    sentiment = ""
    angle = math.atan2(v, a)
    pi = math.pi
    if(0 <= angle < pi / 8):
        sentiment = "pleased"
    if(pi / 8 <= angle < pi / 4):
        sentiment = "happy"
    if(pi / 4 <= angle < pi / 3):
        sentiment = "delighted"
    if(pi / 3 <= angle < pi / 2):
        sentiment = "excited"
    if(angle == pi / 2):
        sentiment = "astonished"
    if(pi / 2 < angle < 2 * pi / 3):
        sentiment = "alarmed"
    if(2 * pi / 3 <= angle < 3 * pi / 4):
        sentiment = "mad"
    if(3 * pi / 4 <= angle < 5 * pi / 6):
        sentiment = "angry"
    if(5 * pi / 6 <= angle < pi):
        sentiment = "annoyed"
    if(pi <= angle < 7 * pi / 6):
        sentiment = "miserable"
    if(7 * pi / 6 <= angle < 5 * pi / 4):
        sentiment = "depressed"
    if(5 * pi / 4 <= angle > 4 * pi / 3):
        sentiment = "bored"
    if(4 * pi / 3 <= angle < 3 * pi / 2):
        sentiment = "tired"
    if(3 * pi / 2 <= angle < 5 * pi / 3):
        sentiment = "sleepy"
    if(5 * pi / 3 <= angle < 7 * pi / 4):
        sentiment = "relaxed"
    if(7 * pi / 4 <= angle < 11 * pi / 6):
        sentiment = "calm"
    if 11 * pi / 6 <= angle < 0:
        sentiment = "content"
    # machine learning is just if statements
    return sentiment


def naive_bayes_demo():
    classifier = NaiveBayes.NaiveBayesClassifier()

    testdata = "These are some sentences. I love writing sentences. Sometimes when I write sentences, I get sad. " \
               "I hope someday to write a sentence all on my own. Some people say that sentences are not real."

    result = []
    loss = classifier.test()
    for sentence in sent_tokenize(testdata):
        sentiment =classifier.analyzeSentiment(sentence)
        result.append(sentence + "vad" + str([x for x in sentiment]))

    print(result)
    print("loss: ", loss)

def lstm_demo():

    testdata = "These are some sentences. I love writing sentences. Sometimes when I write sentences, I get sad. " \
               "I hope someday to write a sentence all on my own. Some people say that sentences are not real."

    classifier = LSTMClassifiers.LSTMClassifier()

    sentences = sent_tokenize(testdata)
    v, a, d = classifier.predict(sentences)


    for i in range(len(sentences)):
        print(sentences[i])
        print("valence: ", v[i])
        print("arousal: ", a[i])
        print("dominance: ", d[i])

if __name__ == "__main__":
    lstm_demo()
    #naive_bayes_demo()