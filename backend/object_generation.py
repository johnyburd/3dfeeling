# python library stuff (not made by us)
import asyncio
import concurrent.futures
from nltk import sent_tokenize
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
from math import ceil
import cProfile

# libraries made by us for this project
import nlp.SentimentClassifier as VAD
import LSTMClassifiers
from ShapeRepresentation.shape import generate_cylinder

# sentiment classifier with 3 dimensions (Valence, Arousal, Dominance)
vad_classifier = VAD.VADClassifier('nlp/emobank.csv')

# above is outdated. should be:
#vad_classifier = LSTMClassifiers.LSTMClassifier()


def graphs(points, fig_id):
    x_values = [i for i in range(1, len(points) + 1)]
    points = np.array(points)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.xlabel('Sentence')
    plt.ylabel('VAD Level')
    ax.plot(x_values, points[:, 0], 'ro-', label='Valence')
    ax.plot(x_values, points[:, 1], 'go-', label='Arousal')
    ax.plot(x_values, points[:, 2], 'bo-', label='Dominance')
    plt.legend()
    ax.set_facecolor("#F6F7F9")
    fig.savefig("../assets/" + fig_id + ".png", facecolor="#F6F7F9",
                edgecolor="#F6F7F9", bbox_inches='tight')


def generate(text):
    """
    Takes a string of text and transforms it into a physical 3D printable model.

    text -- python string of text to be transformed

    This function will fail and error out if an empty string is passed to it. Make sure there
    is at least one sentence in the string before calling this function.
    """
    points = []
    sents = sent_tokenize(text)
    if len(sents) == 1:
        sents.append(sents[0])
        points = [vad_classifier.analyzeSentiment(s) for s in sents]
    elif len(sents) > 2000:
        window = ceil(len(sents) / 2000)
        for i in range(0, len(sents) - window, window):
            vals = np.array([vad_classifier.analyzeSentiment(sents[i + j]) for j in range(window)])
            avg = np.sum(vals, axis=0) / window
            points.append([avg[0], avg[1], avg[2]])
        for i in range(len(sents) - window, len(sents)):
            points.append(vad_classifier.analyzeSentiment(sents[i]))
    else:
        points = [vad_classifier.analyzeSentiment(s) for s in sents]

    model = generate_cylinder(points, 250)

    file_id = str(time.time() * 1000)[0:13]
    filename = "../assets/" + file_id

    model.write(filename + ".scad")
    try:
        subprocess.run(["openscad", "-o", f"{filename}.stl", f"{filename}.scad"])
    except FileNotFoundError:
        print("Please install openscad! STL not generated!")

    graphs(points, file_id)

    return f"{file_id}.stl", points


async def get_object(text):
    """
    Runs the above generate method in a separate thread and awaits the result.
    """
    loop = asyncio.get_running_loop()
    result = ""

    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, generate, text)

    return result

if __name__ == "__main__":
    paragraph = "This is a fun and happy sentence. " * 32000
    cProfile.run("generate(paragraph)")
