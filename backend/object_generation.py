# python library stuff (not made by us)
import asyncio
import concurrent.futures
from nltk import sent_tokenize
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np

# libraries made by us for this project
import nlp.SentimentClassifier as VAD
from ShapeRepresentation.shape import generate_terrain

# sentiment classifier with 3 dimensions (Valence, Arousal, Dominance)
vad_classifier = VAD.VADClassifier('nlp/emobank.csv')


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
    fig.set_facecolor("#F2F2F2")
    ax.set_facecolor("#F2F2F2")
    plt.savefig("../assets/" + fig_id + ".png", bbox_inches='tight')


def generate(text):
    """
    Takes a string of text and transforms it into a physical 3D printable model.

    text -- python string of text to be transformed

    This function will fail and error out if an empty string is passed to it. Make sure there
    is at least one sentence in the string before calling this function.
    """
    points = [vad_classifier.analyzeSentiment(sentence) for sentence in sent_tokenize(text)]
    if len(points) == 1:
        points.append(points[0])
    model = generate_terrain(points, 250)

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
    """
    paragraph = ("Even before Erica finished formally adjourning the meeting, I wove my way through"
                 " the crowd of garrulous people and up the stairs into my bedroom. I grabbed my laptop from the"
                 " desk, then knocked on Ana’s door. She was there waiting for me.")

    asyncio.run(get_object(paragraph))
    """
    graphs(np.random.random((10, 3)), "test")
