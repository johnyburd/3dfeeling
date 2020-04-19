# 3DFeeling
3DFeeling is a website that allows anyone to transform text into a 3D object that represents the emotions contained in that text.

The website uses an NLP model that predicts the Valence, Arousal, and Dominance (VAD) in each sentence and uses those values to generate a unique 3D object that represents those values. You can read more about emotion classification [here](https://en.wikipedia.org/wiki/Emotion_classification).

## NLP Model
The previous NLP model used a [bag-of-words](https://en.wikipedia.org/wiki/Bag-of-words_model). This bag of words was then fed into a [naïve bayes classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) which output the VAD levels of each sentence.

The current NLP model uses 25 dimensional Glove embeddings trained on twitter data. The features are classified using three LSTM (Long Short-Term Memory) models that predict the VAD values for each sentence.

## Object Generation
The first method of object generation was to simply create a 3D histogram of the VAD level in each sentence. This was used as a proof of concept model generation technique and as a stepping stone to more complicated techniques.

The current object generation algorithm that you can see now generates a terrain where each ridge represents the emotion in each sentence. A custom formula takes into account the VAD variables to generate a curve that represents the emotion in that sentence. Many points are then sampled from this curve which are put into the object. These are then all connected together to generate a terrain that represents the entirety of emotion in the text.

## 3D Feeling Release 1.0.0 Notes
### New Features!
Website platform
Upload text or text files to web-service
Three dimensional emotion classification for text: valence, arousal, dominance
View the graph of the three dimensions of emotion classification from sentence to sentence
View 3D model of emotion on the website
Users can download the .stl file of the 3D model
Color recommendation
Ability to choose light or dark theme!
Project information on the website
			
### Bug fixes
Navigation bar at top of web app stops cutting off text when resized
Link to details page in navigation bar functions properly

### Known bugs and defects
STL viewer does not update theme instantaneously upon light/dark theme change, so it will be the opposite of the theme unless the page is refreshed. This actually provides a nice contrast to view the shape so it was kept
STL viewer takes a while to load large STL files
Color recommendation only provides a narrow range of gray colors
Website does not function properly on iOS devices and Safari on Mac computers. We were unable to test how extensive the problem is as we only discovered it very close to release. If the browser immediately refreshes the page after submission instead of taking you to a loading screen you should use another device/browser. 
  
## Website Access
https://3dfeeling.ga/
Pre-requisites: A device with a browser and an internet connection. That’s it!
Dependent libraries that must be installed: None
Download instructions: None
Build Instructions: None
Installation of actual application: None. It’s a web app accessible to everyone
Run Instructions: Type or upload text to the text fields. Click the submit button and wait to view your results.

## Local Install Guide
If you desire to run the classifiers on a local device, or wish to host the project.
Pre-requisites: python-3.6, emobank, glove twitter 25 dimensional, yarn
Dependent libraries that must be installed: aiohttp, aiohttp_cors, nltk, pandas, dill, openpyscad, python-magic, matplotlib, tensorflow==1.5, keras==2.1.5
Download instructions: Clone the project from github then install the prerequisite guide
Build Instructions: We used yarn to build our project and develop the frontend. Install required dependencies with yarn add <dependency> and then build with yarn build. 
Installation of actual application: None. Instead, you need to install dependencies and then run the application as directed by these other points. 
Run Instructions: The backend files can be run by calling python3 <filename.py>. To host the app locally, use yarn start. You may also use other libraries to run it like npm if you are familiar with them.
