# python library stuff (not made by us)
import asyncio
import concurrent.futures
from nltk import sent_tokenize
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
from math import ceil
from multiprocessing import Process, Queue

# libraries made by us for this project
# import LSTMClassifiers
# import nlp.LSTMClassifiers as VAD
from ShapeRepresentation.shape import polygon_cylinder

# sentiment classifier with 3 dimensions (Valence, Arousal, Dominance)
# vad_classifier = VAD.LSTMClassifier()

# above is outdated. should be:
from nlp.LSTMClassifiers import LSTMClassifier


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


def generate(in_queue, out_queue):
    """
    Takes a string of text and transforms it into a physical 3D printable model.

    text -- python string of text to be transformed

    This function will fail and error out if an empty string is passed to it. Make sure there
    is at least one sentence in the string before calling this function.
    """
    vad_classifier = LSTMClassifier()
    while True:
        points = []
        text = in_queue.get(block=True, timeout=None)
        sents = sent_tokenize(text)
        if len(sents) == 1:
            sents.append(sents[0])
            v, a, d = vad_classifier.predict(sents)
            points = np.array([v.flatten(), a.flatten(), d.flatten()]).T
        elif len(sents) > 1000:
            v, a, d = vad_classifier.predict(sents)
            v, a, d = v.flatten(), a.flatten(), d.flatten()
            step = ceil(len(sents) / 1000)
            for i in range(0, len(sents), step):
                points.append([v[i], a[i], d[i]])
            points = np.array(points)
        else:
            v, a, d = vad_classifier.predict(sents)
            points = np.array([v.flatten(), a.flatten(), d.flatten()]).T

        model = polygon_cylinder(points, 250)

        file_id = str(time.time() * 1000)[0:13]
        filename = "../assets/" + file_id

        model.write(filename + ".scad")
        try:
            subprocess.run(["openscad", "-o", f"{filename}.stl", f"{filename}.scad"])
        except FileNotFoundError:
            print("Please install openscad! STL not generated!")

        graphs(points, file_id)

        arg = np.argmax(np.square(points - 0.5), axis=0)
        r = points[arg[0]][0] * 255
        g = points[arg[1]][1] * 255
        b = points[arg[2]][2] * 255
        r, g, b = hex(int(r))[2:], hex(int(g))[2:], hex(int(b))[2:]
        if len(r) != 2:
            r = "0" + r
        if len(g) != 2:
            g = "0" + g
        if len(b) != 2:
            b = "0" + b

        out_queue.put_nowait((f"{file_id}.stl", points.tolist(), "#" + r + g + b))
    # return f"{file_id}.stl", points.tolist(), "#" + r + g + b


create_queue = Queue(maxsize=5)
value_queue = Queue(maxsize=5)
p = Process(target=generate, args=(create_queue, value_queue))
p.start()


async def get_object(text):
    """
    Runs the above generate method in a separate thread and awaits the result.
    """
    create_queue.put_nowait(text)
    result = value_queue.get(block=True, timeout=None)

    return result

if __name__ == "__main__":
    paragraph = """
On the right side of our cranium
Lived the voice of gods and goddesses
Who laid siege to mighty Ilium
And instructed brave Odysseus

Zombie Incas and Assyrians
Knew no humor or morality
Just unquestioning obedience
To their own bicamerality

To this day subconscious processes
Guide the bulk of our activity
So it was. Unconscious Rameses
Had no need for subjectivity

What then, our subjective faculty,
Conscious mind, what is it better for?
It’s an analog reality
We build up in verbal metaphor

We can think in counterfactuals
Play in our imaginations
A replacement for the actual
Audible hallucinations

In our heads reigns quiet loneliness
Where once voices rang, ephemeral
That’s the origin of consciousness
In the mind that was bicameral
"""
    create_queue.put_nowait(paragraph)
    result = value_queue.get(block=True, timeout=None)
