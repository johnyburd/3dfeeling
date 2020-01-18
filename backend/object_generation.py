# python library stuff (not made by us)
import asyncio
import concurrent.futures
from nltk import sent_tokenize
import subprocess
from uuid import uuid4

# libraries made by us for this project
import nlp.SentimentClassifier as VAD
from ShapeRepresentation import shape

# sentiment classifier with 3 dimensions (Valence, Arousal, Dominance)
vad_classifier = VAD.VADClassifier()


def generate(text):
    """
    Takes a string of text and transforms it into a physical 3D printable model.

    text -- python string of text to be transformed

    This function will fail and error out if an empty string is passed to it. Make sure there
    is at least one sentence in the string before calling this function.
    """
    points = [vad_classifier.analyzeSentiment(sentence) for sentence in sent_tokenize(text)]
    model = shape.Representation(points)

    filename = str(uuid4())
    filename = "../assets/" + filename

    model.get_final_shape().write(filename + ".scad")
    subprocess.run(["openscad", "-o", filename + ".stl", filename + ".scad"])

    return filename + ".stl"


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
    paragraph = ("Even before Erica finished formally adjourning the meeting, I wove my way through"
                 " the crowd of garrulous people and up the stairs into my bedroom. I grabbed my laptop from the"
                 " desk, then knocked on Ana’s door. She was there waiting for me.")

    asyncio.run(get_object(paragraph))
