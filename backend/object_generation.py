# python library stuff (not made by us)
import asyncio
import concurrent.futures
from nltk import sent_tokenize
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
from math import ceil

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


def generate(text):
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
    loop = asyncio.get_event_loop()
    result = ""

    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, generate, text)

    return result

if __name__ == "__main__":
    paragraph = """
Life is out there, it is all around me.  But I am dead.  I cannot live.  This is not life.  I still want to live, I want to get better.  I can’t though, nobody can help me.  I hate my life, I hate it.  People will keep talking after I am gone, they will say all of their words, words, words.  The cripples will say their words and others will believe them.  Some of them will be true but many of them won’t.  The “happy” ones will receive gratitude for sparing others the trouble of thinking about the truth.  How many careers have been made by sparing others that trouble?  How many ideas have been loved, how many religions have spread like wildfire for having that capacity?
Death is your end- Mr. Jangley Bones, clattering and clacking.  Am I scared?  I don’t know.  Can one live out of habit?  I just looked at the knife and wondered why I don’t just do it.  Then I thought maybe it was my habit not to kill myself.  Like James said, habits run deep and are highly general.  Crease a piece of paper and it will acquire the habit of being folded, its fibers will take on that habit.  All I have ever done has been to live.  I have only ever pushed myself upwards or toward goals.  I think part preparing for killing myself has been to acquire habits that push me towards it.  I see the decision clearly but have had to slowly push myself to act in accordance with it.  I haven’t been able to quit life cold-turkey, probably because I was so attached to it.  I had the mind of one who was wildly in love with his life and in a moment my life was taken away from me.  So I have had to push myself toward death as if it were a goal when in fact it is no goal at all.  So now I stand in front of that goal I have set for myself and see that there is nothing there, just as I have always known there was nothing there.  So how was I even able to push myself toward it?  Again, with no goal where is the motivation?
The last time I wrote about killing myself, when I was going to try and hang myself, the pain and fear were far greater.  I don’t feel as much pain and fear now but is that only because I am not as close?  Or am I closer and just more indifferent?  I thought I was perhaps very close an hour ago but now I’m not so sure.  It’s a leap, how does one know how close one is?  Or does one just all of a sudden know?  I heard a story of a man who announced that he was going to kill himself then went outside and did it straight away.  Will I only know that point when I get there?  What will that be like?  There is nowhere for me to go now.  I can only go back to the life I hate.  I have to die.  There is no choice.
Lady Macbeth did not want her keen knife to see the wound it made.  Can I watch the knife go in or should I not look?  It’s going to be a lot of blood.  I’m tired.  My arms feel weak.  It’s getting hard to type.  Why does this feel so familiar?  They talk of your life flashing in front of your eyes and every time my imagination gets close I feel something like déjà vu.  I think I may have described this already, but scenes from my youth flash in front of me.  But it’s not just that, but the intensity of the moment brings things back.  I feel like I’m facing a challenge remarkably similar to so many other challenges I have felt in my life.  Such a feeling of familiarity.
I wonder if the feeling I get after I cut myself might even be one of the whole thing being mundane.  Richard Feynman said he would not have wanted to die twice because it was so boring.  I liked Feynman.  So what do I want it to be like?  I don’t expect to like it and I don’t expect any feelings of triumph though I have hoped for that at times.  I have hoped that I would feel liberated and powerful, as if it were a tremendous act of defiance and contempt for a life that I despised.  So many of those kinds of feelings are going away now.  I think in many ways they were expressions of the life inside of me, still wanting to fight, still wanting to win and conquer.  But there is no fight and there is no winning.  That’s one of the essential truths for me in this whole thing and I hope it has been grasped.  Again, the whole thing has nothing to do with strength, courage, perseverance, or any of those kinds of things.  I said already that I see almost zero probability of me ever being cured.  So since I see in being a paraplegic no life that I could possibly accept or be happy with, there is no fighting.  I want to fight but one fights for something.  Being paraplegic is not a life I can fight for because I hate it.  I want a fighting chance.  I can’t live life in chains that will never come off.  All I can hope for is to become happy with a life that now tortures me.  One that cages me, pens me in, puts up walls all around me.  One that makes me smaller, misshapen, that boxes my heart and spirit inside of me.  But that’s no hope at all, no challenge at all.  As if one could say, “You will be enslaved from now on with no chance of escape.  Your owner will use your wife and daughters as he pleases, for his pleasure.  If you do not work you will be whipped and tortured and it will be the same for your family.  Your hope in life, and your challenge, is to become happy with this.”  But that’s no hope at all, no challenge at all.  Still, a slave can hope for freedom, he can dream of the day he will be free and that can perhaps sustain him in part because it is a real possibility.  All that needs to change is something very concrete and simple to understand.  The master can take off the shackles and it is done.  What could give me my freedom is something nobody understands.  Nobody can free me.  Probably the life of a deaf man would be good enough for me, or that of a mute or a man missing a leg or an arm.  But not the life of a paraplegic.  There is not enough left for me.  Too much of what I love is gone or held at a distance forever, too constantly am I forced against my will, painfully frustrated, or deprived of what I want.
And are there still those out there who will say there is something “wrong” with me because of all this?  How unjust those people are to me.  Those people, it seems to me, would lock a wild animal in a tiny cage and find fault with it for experiencing the most horrible agony.  That I could be viewed as somehow defective seems to me the most monstrous and inhuman of truths.  But it’s stronger than that, because I know there will be those out there who despise me for some of the things I have said.
At the end of Camus’ “Stranger” the main character says:
“As if that blind rage had washed me clean, rid me of hope; for the first time, in that night alive with signs and stars, I opened myself to the gentle indifference of the world. Finding it so much like myself- so like a brother, really- I felt that I had been happy and that I was happy again. For everything to be consummated, for me to feel less alone, I had only to wish that there be a large crowd of spectators the day of my execution and that they greet me with cries of hate.”
I mention this because I have found it almost reassuring at times when I have thought of how abandoned I feel by the world, or how despised many of the things I have said will be.  But my life and feelings are not consistent with that theme.  I purposely kept certain kinds of anger alive in me because I thought that was right, but on the whole I did not get pleasure from despising but rather from loving what I thought was great.  So perhaps in those moments the reassurance I felt was something like “You are truly alone in this Clayton, therefore allow yourself some peace.”  I’m not like Camus character in that I am not indifferent at all.  I’ve said it before, I am passionately attached to many things in life.  I want to live.  I want to be healed this moment, finish school, do amazing and wonderful things, have a family, have a house, have grandchildren, and live to be ninety.  I want to live.  I want to live.
How horrible this life is and how sad I am over it.  How hard and strange it is to die.  I really never stop being surprised that so many of you can believe in God and believe that he loves us and cares about us.  How could you believe such a thing?  How can you thank God for the food on your table or because he made you hit a home run but not blame him for the horrible suffering he allows?  Why the praise but not the blame?  I never seem to hear “God I can’t accept you helping me to hit home runs while millions of people are suffering in unbelievable agony.  You are supposed to be all-powerful so I see no reason you couldn’t help everyone if you chose.  I perhaps cannot understand your plan, but as long as children have leukemia I would strongly prefer if you spent your time there and just let me be a mediocre baseball player because I cannot in good conscience be party to your plan so long as it prefers my baseball skills to the healing of children with cancer.”
God loves us?  Aren’t people ashamed to say such things?  Knowledge is a slippery thing in itself but it seems to me that most people know on some level that we are on our own.  God is not helping us.  No omnipotent being in the sky loves us.  But it’s precisely that kind of belief that causes people like me to end up abandoned.  My being a paraplegic is part of God’s plan for me.  It has happened for a reason and it is not up to me to question it by taking my own life.  And on and on, it’s primarily religious sorts of reasons that stand behind euthanasia laws.
So now all of this writing has diverted me from my purpose and I am not in the right state of mind anymore.  If you think it is easy to procrastinate on a school assignment, try killing yourself some time.  I imagine the feeling of the knife going in will be hollow, something like gutting a fish.  The outside is tough but the insides are soft so you feel like you are cutting into something hollow when you slit its belly open.  I think about wrapping the handle of the knife so I don’t feel it and don’t have to even look at it.  I will maybe just see the blood and then feel the light-headedness before I lose consciousness.  “Now, really?  Now?”  That is what I think.
Fuck I did it.  I stabbed myself.  I’m bleeding.  I can’t believe it.  I’m shaking but not scared.  Just don’t know what to think.  I don’t know if I’m bleeding enough but I got myself pretty good.  There is a lot of blood but maybe not enough.  It’s not stopping though so that’s good.  I hope it will take a little time because I want to experience it.  I want to stay in control.  This is my moment.
It’s not so bad to be dying.  Am I still lying to myself?  I guess I don’t know.  I am starting to feel a little funny.  It’s not what I expected, I feel completely normal.  I had to put the knife in slowly, a little at a time because it was hard.  What made me able to do it was just the feeling that there was nothing to go back to.  That life as I have been living it would just be more weeks and endless years of pain for me.  I think I might be feeling a little dizzy.  Honestly I could have a normal conversation right now while I am bleeding to death.  Haha, I just laughed.  I’m smiling.  It’s funny.  This is what I wanted.  I wanted to be okay with dying and I am.  Still smiling.  The wound stopped bleeding as much so I had to try and pull it open with my hand.  I don’t want to cut again, I want this one to do it.  I’ve lost a lot of blood so I hope this does it. 
I cut again.  I got the artery this time.  It’s pumping out, not much time.  What can I say?  Life has been everything to me.  Was it good or bad?  It was just life, everything was in it.  I’m glad I lived and wish I could have lived more.  I think I’m having tachycardia, I’m not sure.  The pumping slowed, maybe it wasn’t the femoral, no I guess it wasn’t.  When I put the knife in the first time I felt bone on the other side, maybe my ileum, so I thought I got all the way through.  I’m bleeding good enough though so I don’t think I have to get in and end it too fast with the femoral if that’s what I missed.
I’m really surprised at how unconcerned I am about this.  I look at the wound, a big, gaping stab hole in my stomach, and it doesn’t really bother me in the least.  This was not what I expected everyone.  Maybe think of me when the time for you to die is coming and be reassured because it’s not so bad at all.  In fact, it’s not bad at all.  The time leading up to it was what was horrible.  As Nietzsche says:
He who exults at the stake, does not triumph over pain, but because of the fact that he does not feel pain where he expected it. A parable.
It’s true friends.  It’s like that with so many things is life.  We spend so much time fearing things but then when we are face-to-face with them we find we had nothing to fear all along.  I’m glad to be talking to all of you now but I guess in the end I don’t need anyone to comfort or help me.  I still suppose it might have been nice to say goodbye in person instead of like this.  I suppose my advice for the living might just be: Live!  And when it is time to die, die!
I’m still feeling fine, maybe I’m not bleeding enough.  I just don’t see how I could live indefinitely with a wound like that.  I know the people I love are going to be so upset about this but there is no need!  Please, don’t!  I’m fine and everything you should be feeling badly about is behind me now.  All of my suffering is over and it was horrible, nightmarish torture that I went through for the last year.  It’s okay now.  I have no fear, it is only sadness because of everything I still wanted to do but as I’ve said so many times all of that was gone anyway.
Part of what I wanted in desiring to die in the company of those I loved was to reassure them and perhaps give them courage to face death well.  That was something I really wanted to give to them and I’m sorry I can only do it with these words.  I was driven almost mad by all of the things many other people said about paraplegia, suicide, and what was still possible in my condition.  I hope everyone understands how all of that affected the tone of what I wrote.  I was so frustrated with all of it, I thought it was so insane.  But I only wanted to break free of it all and say what I felt.  I felt like it stifled me so horribly.
I cut some more and the blood is flowing well again.  I’m surprised how long it is taking me to even feel anything.  I thought I was dizzy but I’m not sure I am now.  It’s 8:51 pm.  I thought I would get cold but I’m not cold either, I’m actually hot but that’s probably the two sweaters.  Starting to feel a little badly.  Sweating, a little light-headed.
I’m going to go now, done writing.  Goodbye everyone.
"""
    create_queue.put_nowait(paragraph)
    result = value_queue.get(block=True, timeout=None)
