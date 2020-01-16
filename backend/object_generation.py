import asyncio
import concurrent.futures
from ShapeRepresentation import shape
import nlp.SentimentClassifier as VAD

vad_classifier = VAD.VADClassifier()

def generate(text):
    return vad_classifier.analyzeSentiment(text)


async def get_object(text):
    loop = asyncio.get_running_loop()

    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, generate, text)
        print(result)

if __name__ == "__main__":
    asyncio.run(get_object("It is a cruel world out there."))
