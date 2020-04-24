import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import numpy as np
import math
from tqdm import tqdm
import corr
import StemPorter 

def normalize(target):
    All = 0
    for i in target:
        # print("a ", int(i))
        All += int(i)
    
    return [float(i) / All for i in target]        


def corr_text(text):
    ans = ""
    
    for i in text.splitlines():
        for j in i.split():
            j = StemPorter.Stem(j)
            j = corr.checkWord(j)
            j = j.lower()
            ans += j.strip()
            if(len(j) > 0 and j != " "):
                ans += " "
    return ans

Base = {}
AllPoints = []

# dict [x,y,z]:class
def loadBase():
    with open("BD_Med_Sport_Math/Sport/SportPoints.txt", "r", encoding = "utf-8") as inpt:
        for i in inpt.readlines():
            tmp = i.split()
            Base[i.strip()] = "Sport"
            AllPoints.append(tmp)
            
    with open("BD_Med_Sport_Math/Med/MedPoints.txt", "r", encoding = "utf-8") as inpt:
        for i in inpt.readlines():
            tmp = i.split()
            Base[i.strip()] = "Med"
            AllPoints.append(tmp)
            
    with open("BD_Med_Sport_Math/Math/MathPoints.txt", "r", encoding = "utf-8") as inpt:
        for i in inpt.readlines():
            tmp = i.split()
            Base[i.strip()] = "Math"
            AllPoints.append(tmp)
            

def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    
    return corr_text(root.text).split()
            
def calcScore(url, text = False):
    if(text == False):
        tmp = get_text(url)
    else:
        tmp = url
    
    tmp = [i.strip() for i in tmp]
    
    SportScore = 0
    BioScore = 0
    MathScore = 0
    cnt = 0
    
    for i in SportTerms:
        CountWords = tmp.count(i)
        if CountWords != 0:
            SportScore += CountWords
    
    for i in BiosTerms:
        CountWords = tmp.count(i)
        if CountWords != 0:
            BioScore += CountWords
    
    for i in MathTerms:
        CountWords = tmp.count(i)
        if CountWords != 0:
            MathScore += CountWords
    
    
    All = SportScore + BioScore + MathScore
    
    # return [(SportScore / All * 100), (BioScore / All * 100), (MathScore / All * 100)]
    return [(SportScore), (BioScore), (MathScore)]
    

def norma(a, b):
    
    if(len(set(a) & set(b)) == 3):
        return 1e10
    
    A = normalize(a)
    B = normalize(b)
    
    ans = 0
    for i in range(3):
        ans += float(A[i]) * float(B[i]) * float(A[i]) * float(B[i])
    return ans


SportTerms = []
with open("BD/Sport/SportTerms.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            SportTerms.append(j)

MathTerms = []
with open("BD/Math/RealMathTerms.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            MathTerms.append(j)
            
BiosTerms = []
with open("BD/Biologic/Bio.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            BiosTerms.append(j)

print("OUT")

loadBase()

SPORT = "BD_Med_Sport_Math/Sport/"
MEDIC = "BD_Med_Sport_Math/Med/"
MATH = "BD_Med_Sport_Math/Math/"

# SPORT = "BD_articles/SportArticles"
# MEDIC = "BD_articles/MedArticles"
# MATH = "BD_articles/MathArticles"

LABELS = {SPORT:0, MEDIC: 1, MATH: 2}
FORLOSS = {0: "Sport", 1:"Med", 2:"Math"}


bestLoss = 10000
bestQ = 0.9


listK = []
lossK = {}

k = 7
loss = 0
for label in LABELS:
        
    for f in tqdm(os.listdir(label)):
        
        if("Point" in f or "_" not in f):
        # if("Point" not in f):
            pass
        else:
            
            path = os.path.join(label, f)
           
            with open(path, "r", encoding = "utf-8") as inpt:
                for url in inpt.readlines():
                    scors = {"Sport":0, "Med":0, "Math":0}
                                        
                    # url = url.strip()
                    target = calcScore(url, text = True)
                    # target = url.strip().split()
                    
                    tmp = sorted(AllPoints, key = lambda x: norma(x, target))
                    
                    #print(tmp)
                    
                    cnt = 1
                    maxv = 0
                    maxName = ""
                    
                    for w in range(k):
                        i = tmp[w]
                        word = str(i[0]) + " " + str(i[1]) + " " + str(i[2])
                        scors[Base[word]] += 10 * math.pow(bestQ, cnt)
                        cnt += 1
                        if(maxv < scors[Base[word]]):
                            maxv = scors[Base[word]]
                            maxName = Base[word]
                    if(maxName != FORLOSS[LABELS[label]]):
                        loss+= 1
listK.append(k)
lossK[k] = loss
        
with open("result.txt", "a", encoding = "utf-8") as t:
        
    for i in sorted(listK, key = lambda x: lossK[x]):
       t.write(str(i) + " loss " + str(lossK[i]) + "\n")