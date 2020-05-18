import os
import cv2
import numpy as np
from tqdm import tqdm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


REBUILD_DATA = True


#Создание тренировачных данных при помощи sklearn

class tr():
    SPORT = "BD_articles/SportArticles"
    MEDIC = "BD_articles/MedArticles"
    MATH = "BD_articles/MathArticles"
    LABELS = {SPORT: 0, MEDIC: 1, MATH: 2}
    dataSPORT = []
    dataMEDIC = []
    dataMATH = []
    training_data = []
    SPORTcount = 0
    MEDICcount = 0
    MATHcount = 0
    
    def logicReg(self, data, target):
        
        text = np.array([i["text"] for i in data])
        y = np.array([i["label"] for i in data])
        
        train, test, y_train, y_test = train_test_split(
            text, y, test_size=0.25, random_state= 10)
        vectorizer = CountVectorizer()
        vectorizer.fit(train)

        X_train = vectorizer.transform(train)
        X_test  = vectorizer.transform(test)
        
        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)
        score = classifier.score(X_test, y_test)
        
        print("Accuracy:", score)
           
    
    def make_training_data(self):
        for label in self.LABELS:
            for f in tqdm(os.listdir(label)):
                if("_Ref" not in f):
                    # try:
                        tmp = {}
                        path = os.path.join(label, f)
                        #прочитать тексты и запомнить откуда они
                        with open(path, "r", encoding = 'utf-8') as inpt:
                            words = inpt.read()
                            
                            
                            
                            tmp["text"] = words
                            tmp["sourse"] = label
                            tmp["label"] = 0;
                            # print(tmp)
                            tmp["label"] = 1 if label == self.SPORT else 0
                            self.dataSPORT.append(tmp)
                            tmp["label"] = 1 if label == self.MEDIC else 0
                            self.dataMEDIC.append(tmp)
                            tmp["label"] = 1 if label == self.MATH else 0
                            self.dataMATH.append(tmp)
                                
                    # except Exception as e:
                    #    pass
        #для каждого из классов отельная Логистическая регрессия
        #self.dataSPORT = pd.concat(self.dataSPORT)
        #self.dataMEDIC = pd.concat(self.dataMEDIC)
        #self.dataMATH = pd.concat(self.dataMATH)
        self.logicReg(self.dataSPORT,self.SPORT)
        self.logicReg(self.dataMEDIC,self.MEDIC)
        self.logicReg(self.dataMATH,self.MATH)
        
        
            
            
                
            
            
        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)
        
if REBUILD_DATA:
    t = tr()
    t.make_training_data()