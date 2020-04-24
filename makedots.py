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
    
    for i in tmp.split():
        CountWords = SportTerms.count(i)
        if CountWords != 0:
            SportScore += CountWords
    
    for i in tmp.split():
        CountWords = BiosTerms.count(i)
        if CountWords != 0:
            BioScore += CountWords
    
    for i in tmp.split():
        CountWords = MathTerms.count(i)
        if CountWords != 0:
            MathScore += CountWords
    All = SportScore + BioScore + MathScore
    
    # return [str(SportScore / All * 100), str(BioScore / All * 100), str(MathScore / All * 100)]
    return [str(SportScore), str(BioScore), str(MathScore)]
    
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
with open("BD/Biologic/Bio.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            BiosTerms.append(j)

print("OUT")

loadBase()

SPORT = "BD_articles/SportArticles"
MEDIC = "BD_articles/MedArticles"
MATH = "BD_articles/MathArticles"
LABELS = {SPORT: "BD_Med_Sport_Math/Sport/SportPoints.txt", 
          MEDIC: "BD_Med_Sport_Math/Med/MedPoints.txt",
          MATH: "BD_Med_Sport_Math/Math/MathPoints.txt"}
FORLOSS = {0: "Sport", 1:"Med", 2:"Math"}

loss = 0


for label in LABELS:
    with open(LABELS[label], "w", encoding = "utf-8") as outpt:
        for f in tqdm(os.listdir(label)):
            
            if("Ref" in f):
                pass
            else:
                try:
                    path = os.path.join(label, f)
                    
                    with open(path, "r", encoding = "utf-8") as inpt:
                       
                        
                        url = inpt.read().replace("\n", " ")
                        
                        target = calcScore(url, True)
                        
                        outpt.write(target[0] + " " + target[1] + " " + target[2] + "\n")
                        
                        
                except:
                    pass