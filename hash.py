import hashlib
import os
from tqdm import tqdm

SPORT = "BD_articles/SportArticles"
MEDIC = "BD_articles/MedArticles"
MATH = "BD_articles/MathArticles"
HASHSPORT = "BD_articles/hash/SportArticles"
HASHMEDIC = "BD_articles/hash/MedArticles"
HASHMATH = "BD_articles/hash/MathArticles"
LABELS = {SPORT:0, MEDIC: 1, MATH:2}
HASHLABELS = {SPORT: HASHSPORT, MEDIC:HASHMEDIC, MATH:HASHMATH}
FORLOSS = {0: "Sport", 1:"Med", 2:"Math"}

loss = 0

for label in LABELS:
            for f in tqdm(os.listdir(label)):
                if "_Ref" not in f:
                    with open(os.path.join(label, f), "r", encoding = "utf-8") as inpt:
                        with open(os.path.join(HASHLABELS[label], f), "w", encoding = "utf-8") as outpt:
                            for i in inpt.readlines():
                                put = ""
                                for j in i.split():
                                    j.strip()
                                    put += str(hashlib.md5(j.encode()).hexdigest()) + " "
                                outpt.write(put + " ")
                                