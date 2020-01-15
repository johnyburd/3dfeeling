import asyncio
import concurrent.futures
from ShapeRepresentation import shape
import nlp.SentimentClassifier as VAD

vad_classifier = VAD.VADClassifier()

def generate(text):
    print(vad_classifier.analyzeSentiment(text))


async def get_object(text):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate, text)
        await location = future.result()
        print(location)

if __name__ == "__main__":
    asyncio.run(get_object("It is a cruel world out there."))
