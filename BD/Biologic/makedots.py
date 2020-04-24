import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import numpy as np
import math
from tqdm import tqdm

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

    return root.text
            
def calcScore(url, text = False):
    if(text == False):
        tmp = get_text(url.strip()).replace("\n", " ")
    else:
        tmp = url
    
    SportScore = 0
    BioScore = 0
    MathScore = 0
    cnt = 0
    
    print("aza")
    for i in SportTerms:
        CountWords = tmp.count(i, 0, len(tmp))
        if CountWords != 0:
            SportScore += CountWords
    
    for i in BiosTerms:
        CountWords = tmp.count(i, 0, len(tmp))
        if CountWords != 0:
            BioScore += CountWords
    
    for i in MathTerms:
        CountWords = tmp.count(i, 0, len(tmp))
        if CountWords != 0:
            MathScore += CountWords
    
    print("Спорт ", SportScore)
    print("Медицина ", BioScore)
    print("Математика ",MathScore)
    
    All = SportScore + BioScore + MathScore
    
    return [SportScore, BioScore, MathScore]
    
def norma(a, b):
    return int(a[0]*b[0] + a[1]*b[1] + a[2]*b[2])


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
with open("BD/Biologic/RealBio.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            BiosTerms.append(j)

print("OUT")

loadBase()

SPORT = "BD_articles/SportArticles"
MEDIC = "BD_articles/MedArticles"
MATH = "BD_articles/MathArticles"
LABELS = {SPORT: 0, MEDIC: 1, MATH:2}
FORLOSS = {0: "Sport", 1:"Med", 2:"Math"}

loss = 0

for label in LABELS:
    for f in tqdm(os.listdir(label)):
        
        if("Ref" in f):
            pass
        else:
            try:
                path = os.path.join(label, f)
                
                with open(path, "r", encoding = "utf-8") as inpt:
                    scors = {"Sport":0, "Med":0, "Math":0}
                    
                    url = inpt.read().replace("\n", " ")
                    
                    target = calcScore(url, True)
                    
                    tmp = sorted(AllPoints, key = lambda x: norma(x, target))
                    
                    #print(tmp)
                    
                    cnt = 2
                    maxv = 0
                    maxName = ""
                    
                    for i in tmp:
                        word = str(i[0]) + " " + str(i[1]) + " " + str(i[2])
                        scors[Base[word]] += 100 / math.log(norma(i, target))
                        if(maxv < scors[Base[word]]):
                            maxv = scors[Base[word]]
                            maxName = Base[word]
                    print(maxName)
                    if(maxName != FORLOSS[LABELS[label]]):
                        loss+= 1
            except:
                pass
print("Loss is ", loss)