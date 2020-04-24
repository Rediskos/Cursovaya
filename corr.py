from tqdm import tqdm

alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def checkWord(word):
    ans = ""
    for i in range(len(word)):
        if(word[i] == ' ' or word[i] in alpha):
            ans += word[i]
    return ans
