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
        r, g, b = hex(int(r)).lstrip("0x"), hex(int(g)).lstrip("0x"), hex(int(b)).lstrip("0x")
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
It’s true friends.  It’s like that with so many things is life.  We spend so much time fearing things but then when we are face-to-face with them we find we had nothing to fear all along.  I’m glad to be talking to all of you now but I guess in the end I don’t need anyone to comfort or help me.  I still suppose it might have been nice to say goodbye in person instead of like this.  I suppose my advice for the living might just be: Live!  And when it is time to die, die!
I’m still feeling fine, maybe I’m not bleeding enough.  I just don’t see how I could live indefinitely with a wound like that.  I know the people I love are going to be so upset about this but there is no need!  Please, don’t!  I’m fine and everything you should be feeling badly about is behind me now.  All of my suffering is over and it was horrible, nightmarish torture that I went through for the last year.  It’s okay now.  I have no fear, it is only sadness because of everything I still wanted to do but as I’ve said so many times all of that was gone anyway.
Part of what I wanted in desiring to die in the company of those I loved was to reassure them and perhaps give them courage to face death well.  That was something I really wanted to give to them and I’m sorry I can only do it with these words.  I was driven almost mad by all of the things many other people said about paraplegia, suicide, and what was still possible in my condition.  I hope everyone understands how all of that affected the tone of what I wrote.  I was so frustrated with all of it, I thought it was so insane.  But I only wanted to break free of it all and say what I felt.  I felt like it stifled me so horribly.
I cut some more and the blood is flowing well again.  I’m surprised how long it is taking me to even feel anything.  I thought I was dizzy but I’m not sure I am now.  It’s 8:51 pm.  I thought I would get cold but I’m not cold either, I’m actually hot but that’s probably the two sweaters.  Starting to feel a little badly.  Sweating, a little light-headed.
I’m going to go now, done writing.  Goodbye everyone.
"""
    print(generate(paragraph))
