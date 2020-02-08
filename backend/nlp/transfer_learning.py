import spacy
from spacy.util import minibatch
import random
import torch
import pandas as pd


spacy.require_gpu()
torch.set_default_tensor_type("torch.cuda.FloatTensor")
device = torch.device("cuda")
spacy.util.use_gpu(0)

# IMPORTANT
# to download the pre-trained model:
# $ python -m spacy download en_trf_distilbertbaseuncased_lg
model = spacy.load("en_trf_distilbertbaseuncased_lg")


def read_data(filename='emobank.csv'):
    print("Reading data...")
    # The emobank dataset contains text entries scored for valence, arousal, and dominance.
    eb = pd.read_csv(filename, index_col=0)

    test_docs = []
    train_docs = []
    # 1 / (trainngsplit) will be resrved for testing
    trainingsplit = 5
    trainingcount = 0

    # read emobank
    for index, row in eb.iterrows():
        v = float(row["V"])
        a = float(row["A"])
        d = float(row["D"])
        text = row["text"]
        # transform VAD values from 6 pt positive scale to range[0, 1]
        v = v / 6
        a = a / 6
        d = d / 6
        try:
            if trainingcount % trainingsplit == 0:
                test_docs.append((text, {"cats": {"valence": v, "arousal": a, "dominance": d}}))
            else:
                train_docs.append((text, {"cats": {"valence": v, "arousal": a, "dominance": d}}))

            trainingcount += 1
        except Exception:
            # pandas struggles to read certain strings...
            print("Failed to add text: ", text)
    print("number training examples:", len(train_docs))
    return train_docs, test_docs


dummy_data = [
    ("He told us a very exciting adventure story.", {"cats": {"POSITIVE": 1.0, "NEGATIVE": 0.0}}),
    ("She wrote him a long letter, but he didn't read it.", {"cats": {"POSITIVE": 0.0, "NEGATIVE": 1.0}}),
    ("I am never at home on Sundays.", {"cats": {"POSITIVE": 0.0, "NEGATIVE": 1.0}}),
    ("He ran out of money, so he had to stop playing poker.", {"cats": {"POSITIVE": 0.0, "NEGATIVE": 1.0}}),
]

dummy_test = [["Here is a sentence"]]

train_data, test_data = read_data()
# train_data = dummy_data
# test_data = dummy_test

print(model.pipe_names)  # ["sentencizer", "pytt_wordpiecer", "pytt_tok2vec"]
textcat = model.create_pipe("trf_textcat", config={"exclusive_classes": True})
for label in ("valence", "arousal", "dominance"):
    textcat.add_label(label)
model.add_pipe(textcat)
# model = model.to(device)
optimizer = model.resume_training()

for i in range(3):
    random.shuffle(train_data)
    losses = {}
    for batch in minibatch(train_data, size=8):
        texts, cats = zip(*batch)
        model.update(texts, cats, drop=0.2, sgd=optimizer, losses=losses)
    print(i, losses)

test_sent = ["This is a test sentence."]

sents = [txt for txt, d in test_data]
for txt, doc in zip(sents, model.pipe(sents)):
    print(txt, doc.cats)
