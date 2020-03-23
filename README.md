# 3DFeeling
3DFeeling is a website that allows anyone to transform text into a 3D object that represents the emotions contained in that text.

The website uses an NLP model that predicts the Valence, Arousal, and Dominance (VAD) in each sentence and uses those values to generate a unique 3D object that represents those values. You can read more about emotion classification [here](https://en.wikipedia.org/wiki/Emotion_classification).

## NLP Model
The current NLP model uses a [bag-of-words](https://en.wikipedia.org/wiki/Bag-of-words_model] model to capture the text in each sentence. This bag of words is then fed into a [niave bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) which will otuput the VAD levels of each sentence.

## Object Generation
The first method of object generation was to simply create a 3D histogram of the VAD level in each sentence. This was used as a proof of concept model generation technique and as a stepping stone to more complicated techniques.

The current object generation algorithm generates a terrain where each ridge represents the emotion in each sentence. A formula was created which takes into account the VAD variables to generate a curve that represents the emotion in that sentence. Many points are then sampled from this curve which are put into the object. These are then all connected together to generate a terrain that represents the entirety of emotion in the text.
