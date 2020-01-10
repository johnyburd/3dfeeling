import nlp.SentimentClassifier as SentimentClassifier
import shape
import nltk
from nltk import sent_tokenize
import os


vad_classifier = SentimentClassifier.VADClassifier()
while True:
    text = input("Enter text to be classified: ")
    points = []
    for sentence in sent_tokenize(text):
        vad = vad_classifier.analyzeSentiment(sentence)
        print(sentence)
        print('valence, arousal and dominance: ', vad)
        points.append((vad[0], vad[1]))
    test_shape = shape.Representation(points)
    test_shape.get_final_shape().write("demo.scad")
    os.system("start " + "demo.scad")

