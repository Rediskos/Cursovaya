import os
from tqdm import tqdm

alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def checkWord(word):
    word.replace('\n', " ")
    ans = ""
    for i in range(len(word)):
        if(word[i] == ' ' or word[i] in alpha):
            ans += word[i]
    return ans


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
                   words = checkWord(inpt.read())
                   outpt.write(words)