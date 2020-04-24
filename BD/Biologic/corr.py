from tqdm import tqdm

alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def checkWord(word):
    ans = ""
    for i in range(len(word)):
        if(word[i] == ' ' or word[i] in alpha):
            ans += word[i]
    return ans

           
SportTerms = []
with open("tmp.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        if(i not in SportTerms):
            SportTerms.append(i)

was = []        
with open("ttmp.txt", "w", encoding = "utf-8") as ST:
    for i in SportTerms:
        tmp = checkWord(i).strip()
        if(len(tmp) > 0):
            if(tmp not in was):
                was.append(tmp)
                ST.write(tmp.lower() + "\n")